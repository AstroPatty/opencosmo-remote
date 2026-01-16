from typing import Any, Optional
from weakref import finalize

import grpc
import opencosmo as oc
from opencosmo.column.column import ColumnMask, DerivedColumn

from opencosmo_remote.columns import serialize_derived_column
from opencosmo_remote.filters import serialize_filters
from opencosmo_remote.messages import OpenCosmoQueryStage, OpenStatement, Token
from opencosmo_remote.messages.column_pb2 import WithNewColumnStatement
from opencosmo_remote.messages.query_pb2 import WriteStatement
from opencosmo_remote.messages.query_pb2_grpc import OpenCosmoQueryHandlerStub
from opencosmo_remote.messages.select_pb2 import DatasetSelectStatement
from opencosmo_remote.messages.take_pb2 import TakeRangeStatement, TakeStatement


def open_remote(name: str, dtypes: Optional[list[str]] = []):
    channel = grpc.insecure_channel("localhost:50051")
    stub = OpenCosmoQueryHandlerStub(channel)
    open_statement = OpenStatement(dataset_name=name, dtypes=dtypes)
    resp = stub.OpenRemote(open_statement)

    return RemoteDataset(stub, resp.new_token, resp.message)


def close_remote(stub: OpenCosmoQueryHandlerStub, token: Token):
    stub.CloseRemote(token)


def send(args: dict[str, Any], token: Token, stub: OpenCosmoQueryHandlerStub):
    stage = OpenCosmoQueryStage(token=token, **args)
    resp = stub.DoQueryStage(stage)
    return resp.message


class RemoteDataset:
    def __init__(self, stub: OpenCosmoQueryHandlerStub, token, repr):
        self.__stub = stub
        self.__token = token
        self.__repr = repr
        finalize(self, lambda: close_remote(self.__stub, self.__token))

    def __repr__(self):
        return self.__repr

    def filter(self, *masks: ColumnMask):
        filters = serialize_filters(*masks)
        self.__repr = send({"filter": filters}, self.__token, self.__stub)
        return self

    def select(self, columns: list[str]):
        stmt = DatasetSelectStatement(columns=columns)
        self.__repr = send({"select": stmt}, self.__token, self.__stub)
        return self

    def take(self, n: int, at: str = "random"):
        stmt = TakeStatement(n=n, at=at)
        self.__repr = send({"take": stmt}, self.__token, self.__stub)

    def take_range(self, start: int, end: int):
        stmt = TakeRangeStatement(start, end)
        self.__repr = send({"take_range": stmt}, self.__token, self.__stub)
        return self

    def with_new_columns(self, **columns: DerivedColumn):
        serialized_columns = {
            name: serialize_derived_column(column) for name, column in columns.items()
        }
        stmt = WithNewColumnStatement(columns=serialized_columns)
        self.__repr = send({"new_columns": stmt}, self.__token, self.__stub)
        return self

    def get_data(self):
        stmt = WriteStatement(token=self.__token)
        path = self.__stub.WriteData(stmt)
        return oc.open(path.path)
