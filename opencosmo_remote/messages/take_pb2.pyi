from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TakeStatement(_message.Message):
    __slots__ = ("n", "at")
    class TakeAt(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        START: _ClassVar[TakeStatement.TakeAt]
        END: _ClassVar[TakeStatement.TakeAt]
        RANDOM: _ClassVar[TakeStatement.TakeAt]
    START: TakeStatement.TakeAt
    END: TakeStatement.TakeAt
    RANDOM: TakeStatement.TakeAt
    N_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    n: int
    at: TakeStatement.TakeAt
    def __init__(self, n: _Optional[int] = ..., at: _Optional[_Union[TakeStatement.TakeAt, str]] = ...) -> None: ...

class TakeRangeStatement(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...
