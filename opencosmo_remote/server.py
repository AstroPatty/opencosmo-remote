from concurrent import futures
from enum import Enum
from typing import Callable, TypedDict
from uuid import uuid1

import grpc
from google.protobuf.empty_pb2 import Empty
from mpi4py import MPI

from opencosmo_remote.commands import handle_message
from opencosmo_remote.config import (
    OpenCosmoRemoteFollowerSettings,
    OpenCosmoRemotePointSettings,
    get_settings,
)
from opencosmo_remote.messages import query_pb2, query_pb2_grpc
from opencosmo_remote.messages.open_pb2 import InternalOpenStatement
from opencosmo_remote.messages.query_pb2 import CloseResponse, Token
from opencosmo_remote.store import read


def start(root=0, **kwargs):
    comm = MPI.COMM_WORLD.Dup()
    settings = get_settings(comm, root, **kwargs)
    if comm.Get_rank() == root:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        query_pb2_grpc.add_OpenCosmoQueryHandlerServicer_to_server(
            PointServer(comm=comm, server=server, settings=settings), server
        )
        server.add_insecure_port(f"[::]:{settings.port}")
        server.start()
        server.wait_for_termination()
    else:
        server = FollowServer(comm, settings=settings)
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
    Runs on rank 0, communicates with user and then relays to
    other ranks. Also participates
    """

    def __init__(
        self, *args, comm, server, settings: OpenCosmoRemotePointSettings, **kwargs
    ):
        self.__comm = comm
        self.__datasets = {}
        self.__server = server
        self.__settings = settings
        super().__init__(*args, **kwargs)

    def OpenRemote(self, request, context: grpc.ServicerContext):
        """
        Open a dataset
        """
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

        def make_response(datasets):
            ds = datasets[token.uuid]
            repr = str(ds)
            return query_pb2.QueryResponse(new_token=token, message=repr)

        return self.execute(msg, context, make_response)

    def CloseRemote(self, token, context):
        """
        Close a given remote dataset. Currently we only allow one open
        remote dataset at a time.
        """
        uuid = token.uuid
        if uuid not in self.__datasets:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Unknown token")

        return self.execute(token, context, lambda _: CloseResponse(res="success"))
        self.__comm.bcast(token)
        self.__datasets.pop(uuid)
        return CloseResponse(res="sucess")

    def Exit(self, *args, **kwargs):
        """
        Shut down the server.
        """
        self.__comm.bcast("EXIT")
        self.__server.stop(0)
        return Empty()

    def DoQueryStage(self, request, context):
        """
        This API endpoint handles all query requests.
        """

        def success_callback(datasets):
            repr = str(datasets[request.token.uuid])
            return query_pb2.QueryResponse(repr=repr)

        return self.execute(request, context, success_callback)

    def execute(self, stmt, context, return_on_success: Callable):
        """
        Handle a given request. This includes broadcasting it to the other ranks,
        performing the action on this rank, and checking for errors.
        """
        self.__comm.bcast(stmt)

        try:
            new_datasets, response = handle_message(stmt, self.__datasets)
            result: CommandResult = {
                "status": CommandResultStatus.SUCCESS,
                "response": response,
            }

        except Exception as e:
            result: CommandResult = {
                "status": CommandResultStatus.FAIL,
                "msg": str(e),
            }
        results = self.__comm.allgather(result)
        # All ranks know if any rank failed, and also fail.

        failed = list(
            filter(lambda r: r["status"] != CommandResultStatus.SUCCESS, results)
        )
        if not failed:
            self.__datasets = new_datasets
            return result["response"]
            # Success!

        context.set_code(grpc.StatusCode.ABORTED)
        context.set_details(f"One or more ranks failed: {failed[0]['msg']}")
        return


class FollowServer:
    def __init__(self, comm, settings: OpenCosmoRemoteFollowerSettings):
        """
        Runs on all other ranks and handles commands relayed from the
        point server.
        """
        self.__comm = comm
        self.__datasets = {}
        self.__settings = settings

    def listen(self):
        while (msg := self.__comm.bcast(None, root=0)) != "EXIT":
            try:
                new_handlers, response = handle_message(msg, self.__datasets)
                result: CommandResult = {
                    "status": CommandResultStatus.SUCCESS,
                    "response": response,
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
