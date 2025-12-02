import opencosmo as oc

from opencosmo_remote import messages as m


def execute_message(query: m.OpenCosmoQueryStage, dataset: oc.Dataset) -> oc.Dataset:
    match query.WhichOneof("query"):
        case "select":
            return do_select(query.select, dataset)
        case "filter":
            return do_filter(query.filter, dataset)
        case "take":
            return do_take(query.take, dataset)
        case "take_range":
            return do_take_range(query.take_range, dataset)


def do_select(select_stmt: m.DatasetSelectStatement, dataset: oc.Dataset):
    result = dataset.select(select_stmt.columns)
    return result


def hydrate_filters(filter_stmt: m.FilterStatement) -> list:
    output = []
    for stmt in filter_stmt.filters:
        column = oc.col(stmt.column)
        match stmt.filter_type:
            case m.FilterType.GT:
                output.append(column > stmt.value)
            case m.FilterType.GTE:
                output.append(column >= stmt.value)
            case m.FilterType.LT:
                output.append(column < stmt.value)
            case m.FilterType.LTE:
                output.append(column <= stmt.value)
    return output


def do_filter(filters: m.FilterStatement, dataset: oc.Dataset):
    filter_objs = hydrate_filters(filters)
    return dataset.filter(*filter_objs)


def do_take(take_stmt: m.TakeStatement, dataset: oc.Dataset):
    at = str(take_stmt.TakeAt.Name(take_stmt.at)).lower()

    result = dataset.take(take_stmt.n, at=at)
    return result


def do_take_range(take_range):
    raise NotImplementedError
