from typing import Optional
from weakref import finalize

import grpc
from opencosmo.dataset.column import ColumnMask

from opencosmo_remote.filters import do_filter
from opencosmo_remote.messages import OpenStatement, Token
from opencosmo_remote.messages.query_pb2_grpc import OpenCosmoQueryHandlerStub


def open_remote(name: str, dtypes: Optional[list[str]] = []):
    channel = grpc.insecure_channel("localhost:50051")
    stub = OpenCosmoQueryHandlerStub(channel)
    open_statement = OpenStatement(dataset_name=name, dtypes=dtypes)
    resp = stub.OpenRemote(open_statement)
    return RemoteDataset(stub, resp.new_token)


def close_remote(stub: OpenCosmoQueryHandlerStub, token: Token):
    print(type(token.uuid))
    stub.CloseRemote(token)


class RemoteDataset:
    def __init__(self, stub: OpenCosmoQueryHandlerStub, token):
        self.__stub = stub
        self.__token = token
        print(self.__token.uuid)
        finalize(self, lambda: close_remote(self.__stub, self.__token))

    def filter(self, *masks: ColumnMask):
        response = do_filter(masks, stub=self.__stub, token=self.__token)
        self.__repr = response.repr
        return self
