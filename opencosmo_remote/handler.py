from concurrent import futures
from pathlib import Path
from typing import Optional
from uuid import uuid1

import grpc
import opencosmo as oc

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages import query_pb2_grpc
from opencosmo_remote.messages.query_pb2 import OutputPath, QueryResponse, Token
from opencosmo_remote.paths import get_halo_paths
from opencosmo_remote.store import read


def create_query_handler(
    dataset: str, step: int, data_types: Optional[str | list[str]]
):
    base_path = read(dataset)
    paths = get_halo_paths(base_path, step, data_types, flatten=True)
    return QueryHandler.from_paths(paths)


class QueryHandler(query_pb2_grpc.OpenCosmoQueryHandlerServicer):
    def __init__(
        self,
        *args,
        dataset: oc.Dataset | oc.StructureCollection,
        data_sync: str,
        **kwargs,
    ):
        self.datasets = {}
        self.data_sync = Path(data_sync)
        super().__init__(*args, **kwargs)

    @classmethod
    def from_paths(cls, paths: list[Path]):
        ds = oc.open(*paths)
        return QueryHandler(dataset=ds, data_sync="/")

    def OpenRemote(self, request, context):
        output_id = uuid1()
        token = Token(uuid=str(output_id))
        dataset = oc.open(self.data_source)
        self.datasets[str(output_id)] = dataset
        return token

    def DatasetRoute(self, request, context):
        dataset = self.datasets[request.token.uuid]
        self.datasets[request.token.uuid] = execute_message(request, dataset)
        return QueryResponse(response="Ok")

    def Execute(self, token, context):
        uuid = token.uuid
        output_path = self.data_sync / f"{uuid}.hdf5"
        oc.write(output_path, self.datasets[uuid])
        self.datasets.pop(uuid)
        return OutputPath(path=str(output_path))


def serve_dataset(dataset_path: str, output_path):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    query_pb2_grpc.add_OpenCosmoQueryHandlerServicer_to_server(
        QueryHandler(data_source=dataset_path, data_sync=output_path), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve_dataset(DATA_SOURCE, DATA_SYNC)
