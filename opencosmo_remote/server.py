from concurrent import futures
from enum import Enum
from typing import Callable, TypedDict
from uuid import uuid1

import grpc
from google.protobuf.empty_pb2 import Empty
from mpi4py import MPI

from opencosmo_remote.commands import handle_message
from opencosmo_remote.messages import query_pb2, query_pb2_grpc
from opencosmo_remote.messages.open_pb2 import InternalOpenStatement
from opencosmo_remote.messages.query_pb2 import Token
from opencosmo_remote.store import read


def start(root=0):
    comm = MPI.COMM_WORLD.Dup()
    if comm.Get_rank() == root:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        query_pb2_grpc.add_OpenCosmoQueryHandlerServicer_to_server(
            PointServer(comm=comm, server=server), server
        )
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()
    else:
        server = Server(comm)
        server.listen()


class CommandResultStatus(Enum):
    SUCCESS = 0
    FAIL = 1
    TIMEOUT = 2


class CommandResult(TypedDict):
    status: CommandResultStatus
    msg: str


class PointServer(query_pb2_grpc.OpenCosmoQueryHandlerServicer):
    """
    Runs on rank 0, communicates with user
    """

    def __init__(self, *args, comm, server, **kwargs):
        self.__comm = comm
        self.__datasets = {}
        self.__server = server
        super().__init__(*args, **kwargs)

    def execute(self, stmt, context, return_on_success: Callable):
        self.__comm.bcast(stmt)

        try:
            new_datasets = handle_message(stmt, self.__datasets)
            result: CommandResult = {
                "status": CommandResultStatus.SUCCESS,
                "msg": "",
            }

        except Exception as e:
            result: CommandResult = {
                "status": CommandResultStatus.FAIL,
                "msg": str(e),
            }
        results = self.__comm.allgather(result)
        failed = list(
            filter(lambda r: r["status"] != CommandResultStatus.SUCCESS, results)
        )
        if not failed:
            self.__datasets = new_datasets
            res = return_on_success(self.__datasets)
            return res

        context.set_code(grpc.StatusCode.ABORTED)
        context.set_details(f"One or more ranks failed: {failed[0]['msg']}")
        return

    def OpenRemote(self, request, context: grpc.ServicerContext):
        if len(self.__datasets) > 0:
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            context.set_details("Currently, only one open dataset is allowed at a time")
            return query_pb2.QueryResponse()

        dataset_path = read(request.dataset_name)
        output_id = uuid1()
        token = Token(uuid=str(output_id))
        msg = InternalOpenStatement(
            dataset_path=dataset_path, uuid=str(output_id), dtypes=request.dtypes
        )
        return self.execute(msg, context, lambda _: token)

    def DoQueryStage(self, request, context):
        def success_callback(_):
            return query_pb2.QueryResponse(response="success")

        return self.execute(request, context, success_callback)

    def Exit(self, *args, **kwargs):
        self.__comm.bcast("EXIT")
        self.__server.stop(0)
        return Empty()


class Server:
    def __init__(self, comm):
        self.__comm = comm
        self.__datasets = {}

    def listen(self):
        while (msg := self.__comm.bcast(None, root=0)) != "EXIT":
            try:
                new_handlers = handle_message(msg, self.__datasets)
                result: CommandResult = {
                    "status": CommandResultStatus.SUCCESS,
                    "msg": "",
                }
            except Exception as e:
                result: CommandResult = {
                    "status": CommandResultStatus.FAIL,
                    "msg": str(e),
                }
            results = self.__comm.allgather(result)
            success = all(r["status"] == CommandResultStatus.SUCCESS for r in results)
            # User error communication handled by root
            if success:
                self.__datasets = new_handlers
