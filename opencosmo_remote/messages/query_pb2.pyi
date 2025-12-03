from opencosmo_remote.messages import select_pb2 as _select_pb2
from opencosmo_remote.messages import filter_pb2 as _filter_pb2
from opencosmo_remote.messages import take_pb2 as _take_pb2
from opencosmo_remote.messages import open_pb2 as _open_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenCosmoQueryStage(_message.Message):
    __slots__ = ("token", "select", "filter", "take", "take_range")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    TAKE_FIELD_NUMBER: _ClassVar[int]
    TAKE_RANGE_FIELD_NUMBER: _ClassVar[int]
    token: Token
    select: _select_pb2.DatasetSelectStatement
    filter: _filter_pb2.FilterStatement
    take: _take_pb2.TakeStatement
    take_range: _take_pb2.TakeRangeStatement
    def __init__(self, token: _Optional[_Union[Token, _Mapping]] = ..., select: _Optional[_Union[_select_pb2.DatasetSelectStatement, _Mapping]] = ..., filter: _Optional[_Union[_filter_pb2.FilterStatement, _Mapping]] = ..., take: _Optional[_Union[_take_pb2.TakeStatement, _Mapping]] = ..., take_range: _Optional[_Union[_take_pb2.TakeRangeStatement, _Mapping]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

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
