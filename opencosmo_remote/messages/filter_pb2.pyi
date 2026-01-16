from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GT: _ClassVar[FilterType]
    GTE: _ClassVar[FilterType]
    LT: _ClassVar[FilterType]
    LTE: _ClassVar[FilterType]
    EQ: _ClassVar[FilterType]
    NEQ: _ClassVar[FilterType]
    ISIN: _ClassVar[FilterType]
GT: FilterType
GTE: FilterType
LT: FilterType
LTE: FilterType
EQ: FilterType
NEQ: FilterType
ISIN: FilterType

class ColumnFilter(_message.Message):
    __slots__ = ("column", "filter_type", "value")
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    column: str
    filter_type: FilterType
    value: float
    def __init__(self, column: _Optional[str] = ..., filter_type: _Optional[_Union[FilterType, str]] = ..., value: _Optional[float] = ...) -> None: ...

class FilterStatement(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[ColumnFilter]
    def __init__(self, filters: _Optional[_Iterable[_Union[ColumnFilter, _Mapping]]] = ...) -> None: ...
