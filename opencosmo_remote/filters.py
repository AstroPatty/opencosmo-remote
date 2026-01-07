import operator as op

import opencosmo as oc
from opencosmo.dataset.column import ColumnMask

from opencosmo_remote.messages.filter_pb2 import (
    ColumnFilter,
    FilterStatement,
    FilterType,
)


def hydrate_filters(filter_stmt: FilterStatement) -> list:
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
    return output


def do_filter(filters: FilterStatement, dataset: oc.Dataset):
    filter_objs = hydrate_filters(filters)
    return dataset.filter(*filter_objs)


def serialize_filter(mask: ColumnMask):
    match mask.operator:
        case op.gt:
            operation = FilterType.GT
        case op.lt:
            operation = FilterType.LT
        case op.gte:
            operation = FilterType.GTE
        case op.lte:
            operation = FilterType.LTE
        case _:
            raise ValueError(
                f"Operator {mask.operator} is not supported for remote datasets"
            )

    return ColumnFilter(
        column=mask.column_name, filter_type=operation, value=mask.value
    )
