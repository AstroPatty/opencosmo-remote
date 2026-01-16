import operator as op

import opencosmo as oc
from opencosmo.column.column import ColumnMask

from opencosmo_remote.messages.filter_pb2 import (
    ColumnFilter,
    FilterStatement,
    FilterType,
)


def deserialize_filters(filter_stmt: FilterStatement) -> list:
    """
    Turn filter statement messages into OpenCosmo filters
    """
    output = []
    for stmt in filter_stmt.filters:
        column = oc.col(stmt.column)
        match stmt.filter_type:
            case FilterType.GT:
                output.append(column > stmt.value)
            case FilterType.GTE:
                output.append(column >= stmt.value)
            case FilterType.LT:
                output.append(column < stmt.value)
            case FilterType.LTE:
                output.append(column <= stmt.value)
            case FilterType.EQ:
                output.append(column == stmt.value)
            case FilterType.NEQ:
                output.append(column != stmt.value)
    return output


def serialize_filter(mask: ColumnMask):
    match mask.operator:
        case op.gt:
            operation = FilterType.GT
        case op.lt:
            operation = FilterType.LT
        case op.ge:
            operation = FilterType.GTE
        case op.le:
            operation = FilterType.LTE
        case op.eq:
            operation = FilterType.EQ
        case op.ne:
            operation = FilterType.NEQ
        case _:
            raise ValueError(
                f"Operator {mask.operator} is not supported for remote datasets"
            )

    return ColumnFilter(
        column=mask.column_name, filter_type=operation, value=mask.value
    )


def serialize_filters(*filters: ColumnMask):
    serialized_filters = map(serialize_filter, filters)
    stmt = FilterStatement(filters=serialized_filters)
    return stmt


def do_filters(filters: FilterStatement, dataset: oc.Dataset):
    filter_objs = deserialize_filters(filters)
    return dataset.filter(*filter_objs)
