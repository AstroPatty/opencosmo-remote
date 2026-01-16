from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class operation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADD: _ClassVar[operation]
    SUBTRACT: _ClassVar[operation]
    MULTIPLY: _ClassVar[operation]
    DIVIDE: _ClassVar[operation]
    POW: _ClassVar[operation]
    EXP10: _ClassVar[operation]
    LOG10: _ClassVar[operation]
    SQRT: _ClassVar[operation]
ADD: operation
SUBTRACT: operation
MULTIPLY: operation
DIVIDE: operation
POW: operation
EXP10: operation
LOG10: operation
SQRT: operation

class DerivedColumn(_message.Message):
    __slots__ = ("lhs_scalar", "lhs_derived", "lhs_column", "rhs_scalar", "rhs_derived", "rhs_column", "op")
    LHS_SCALAR_FIELD_NUMBER: _ClassVar[int]
    LHS_DERIVED_FIELD_NUMBER: _ClassVar[int]
    LHS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    RHS_SCALAR_FIELD_NUMBER: _ClassVar[int]
    RHS_DERIVED_FIELD_NUMBER: _ClassVar[int]
    RHS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    lhs_scalar: float
    lhs_derived: DerivedColumn
    lhs_column: str
    rhs_scalar: float
    rhs_derived: DerivedColumn
    rhs_column: str
    op: operation
    def __init__(self, lhs_scalar: _Optional[float] = ..., lhs_derived: _Optional[_Union[DerivedColumn, _Mapping]] = ..., lhs_column: _Optional[str] = ..., rhs_scalar: _Optional[float] = ..., rhs_derived: _Optional[_Union[DerivedColumn, _Mapping]] = ..., rhs_column: _Optional[str] = ..., op: _Optional[_Union[operation, str]] = ...) -> None: ...

class WithNewColumnStatement(_message.Message):
    __slots__ = ("columns",)
    class ColumnsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DerivedColumn
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DerivedColumn, _Mapping]] = ...) -> None: ...
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.MessageMap[str, DerivedColumn]
    def __init__(self, columns: _Optional[_Mapping[str, DerivedColumn]] = ...) -> None: ...
