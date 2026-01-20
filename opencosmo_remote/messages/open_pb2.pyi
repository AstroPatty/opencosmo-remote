from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HALO_PROPERTIES: _ClassVar[DataType]
    HALO_PARTICLES: _ClassVar[DataType]
    HALO_PROFILES: _ClassVar[DataType]
    GALAXY_PROPERTIES: _ClassVar[DataType]
    GALAXY_PARTICLES: _ClassVar[DataType]
    GALAXY_PROFILES: _ClassVar[DataType]
HALO_PROPERTIES: DataType
HALO_PARTICLES: DataType
HALO_PROFILES: DataType
GALAXY_PROPERTIES: DataType
GALAXY_PARTICLES: DataType
GALAXY_PROFILES: DataType

class OpenStatement(_message.Message):
    __slots__ = ("dataset_name", "step_number", "dtypes")
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    STEP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DTYPES_FIELD_NUMBER: _ClassVar[int]
    dataset_name: str
    step_number: int
    dtypes: _containers.RepeatedScalarFieldContainer[DataType]
    def __init__(self, dataset_name: _Optional[str] = ..., step_number: _Optional[int] = ..., dtypes: _Optional[_Iterable[_Union[DataType, str]]] = ...) -> None: ...

class InternalOpenStatement(_message.Message):
    __slots__ = ("dataset_path", "uuid", "step_number", "dtypes")
    DATASET_PATH_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    STEP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DTYPES_FIELD_NUMBER: _ClassVar[int]
    dataset_path: str
    uuid: str
    step_number: int
    dtypes: _containers.RepeatedScalarFieldContainer[DataType]
    def __init__(self, dataset_path: _Optional[str] = ..., uuid: _Optional[str] = ..., step_number: _Optional[int] = ..., dtypes: _Optional[_Iterable[_Union[DataType, str]]] = ...) -> None: ...
