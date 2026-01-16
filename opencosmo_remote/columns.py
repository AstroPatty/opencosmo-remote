import functools
import operator as op

from opencosmo.column import column as _col
from opencosmo.column.column import Column, DerivedColumn

from opencosmo_remote.messages.column_pb2 import (
    DerivedColumn as SerializedDerivedColumn,
)
from opencosmo_remote.messages.column_pb2 import (
    operation,
)


def serialize_derived_column(column: DerivedColumn):
    data = {}
    match column.lhs:
        case Column():
            data["lhs_column"] = column.lhs.column_name
        case DerivedColumn():
            data["lhs_derived"] = serialize_derived_column(column.lhs)
        case None:
            pass
        case _:
            data["lhs_scalar"] = column.lhs
    match column.rhs:
        case Column():
            data["rhs_column"] = column.rhs.column_name
        case DerivedColumn():
            data["rhs_derived"] = serialize_derived_column(column.rhs)
        case None:
            pass
        case _:
            data["rhs_scalar"] = column.rhs

    match column.operation:
        case op.add:
            data["op"] = operation.ADD
        case op.sub:
            data["op"] = operation.SUBTRACT
        case op.mul:
            data["op"] = operation.MULTIPLY
        case op.truediv:
            data["op"] = operation.DIVIDE
        case op.pow:
            data["op"] = operation.POW
        case _:
            data["op"] = try_serialize_function(column.operation)

    assert "op" in data
    return SerializedDerivedColumn(**data)


def try_serialize_function(op_):
    if isinstance(op_, functools.partial):
        op_ = op_.func
    match op_:
        case _col._log10:
            return operation.LOG10
        case _col._exp10:
            return operation.EXP10
        case _col._sqrt:
            return operation.SQRT

    raise ValueError(f"Unsupported operation {op_}")


def deserialize_derived_column(column: SerializedDerivedColumn):
    match column.WhichOneof("lhs"):
        case "lhs_scalar":
            lhs = column.lhs_scalar
        case "lhs_column":
            lhs = Column(column.lhs_column)
        case "lhs_derived":
            lhs = deserialize_derived_column(column.lhs_derived)
    match column.WhichOneof("rhs"):
        case "rhs_scalar":
            rhs = column.rhs_scalar
        case "rhs_column":
            rhs = Column(column.rhs_column)
        case "rhs_derived":
            rhs = deserialize_derived_column(column.rhs_derived)
        case None:
            rhs = None
    match column.op:
        case operation.ADD:
            op_ = op.add
        case operation.SUBTRACT:
            op_ = op.sub
        case operation.MULTIPLY:
            op_ = op.mul
        case operation.DIVIDE:
            op_ = op.truediv
        case operation.POW:
            op_ = op.pow
        case operation.EXP10:
            op_ = _col._exp10
        case operation.LOG10:
            op_ = _col._log10
        case operation.SQRT:
            op_ = _col._sqrt

    return DerivedColumn(lhs, rhs, op_)
