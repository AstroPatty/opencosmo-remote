from opencosmo_remote.messages import select_pb2 as _select_pb2
from opencosmo_remote.messages import filter_pb2 as _filter_pb2
from opencosmo_remote.messages import take_pb2 as _take_pb2
from opencosmo_remote.messages import open_pb2 as _open_pb2
from opencosmo_remote.messages import column_pb2 as _column_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenCosmoQueryStage(_message.Message):
    __slots__ = ("token", "select", "filter", "take", "take_range", "new_columns", "sort_by")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    TAKE_FIELD_NUMBER: _ClassVar[int]
    TAKE_RANGE_FIELD_NUMBER: _ClassVar[int]
    NEW_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    token: Token
    select: _select_pb2.DatasetSelectStatement
    filter: _filter_pb2.FilterStatement
    take: _take_pb2.TakeStatement
    take_range: _take_pb2.TakeRangeStatement
    new_columns: _column_pb2.WithNewColumnStatement
    sort_by: _column_pb2.SortByStatement
    def __init__(self, token: _Optional[_Union[Token, _Mapping]] = ..., select: _Optional[_Union[_select_pb2.DatasetSelectStatement, _Mapping]] = ..., filter: _Optional[_Union[_filter_pb2.FilterStatement, _Mapping]] = ..., take: _Optional[_Union[_take_pb2.TakeStatement, _Mapping]] = ..., take_range: _Optional[_Union[_take_pb2.TakeRangeStatement, _Mapping]] = ..., new_columns: _Optional[_Union[_column_pb2.WithNewColumnStatement, _Mapping]] = ..., sort_by: _Optional[_Union[_column_pb2.SortByStatement, _Mapping]] = ...) -> None: ...

class WriteStatement(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: Token
    def __init__(self, token: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class DatasetSpecification(_message.Message):
    __slots__ = ("length", "columns", "is_lightcone")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    IS_LIGHTCONE_FIELD_NUMBER: _ClassVar[int]
    length: int
    columns: _containers.RepeatedScalarFieldContainer[str]
    is_lightcone: bool
    def __init__(self, length: _Optional[int] = ..., columns: _Optional[_Iterable[str]] = ..., is_lightcone: bool = ...) -> None: ...

class StructureCollectionSpecification(_message.Message):
    __slots__ = ("length", "datasets")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    length: int
    datasets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, length: _Optional[int] = ..., datasets: _Optional[_Iterable[str]] = ...) -> None: ...

class OpenCosmoDataSpecification(_message.Message):
    __slots__ = ("ds", "sc")
    DS_FIELD_NUMBER: _ClassVar[int]
    SC_FIELD_NUMBER: _ClassVar[int]
    ds: DatasetSpecification
    sc: StructureCollectionSpecification
    def __init__(self, ds: _Optional[_Union[DatasetSpecification, _Mapping]] = ..., sc: _Optional[_Union[StructureCollectionSpecification, _Mapping]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("spec", "message", "new_token")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NEW_TOKEN_FIELD_NUMBER: _ClassVar[int]
    spec: OpenCosmoDataSpecification
    message: str
    new_token: Token
    def __init__(self, spec: _Optional[_Union[OpenCosmoDataSpecification, _Mapping]] = ..., message: _Optional[str] = ..., new_token: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class OutputPath(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class OpenResponse(_message.Message):
    __slots__ = ("token", "repr")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    REPR_FIELD_NUMBER: _ClassVar[int]
    token: Token
    repr: str
    def __init__(self, token: _Optional[_Union[Token, _Mapping]] = ..., repr: _Optional[str] = ...) -> None: ...

class CloseResponse(_message.Message):
    __slots__ = ("res",)
    RES_FIELD_NUMBER: _ClassVar[int]
    res: str
    def __init__(self, res: _Optional[str] = ...) -> None: ...
