import opencosmo as oc

from opencosmo_remote import messages as m
from opencosmo_remote.columns import deserialize_derived_column
from opencosmo_remote.filters import do_filters
from opencosmo_remote.messages.column_pb2 import WithNewColumnStatement
from opencosmo_remote.messages.query_pb2 import DatasetSpecification


def execute_message(query: m.OpenCosmoQueryStage, dataset: oc.Dataset) -> oc.Dataset:
    match query.WhichOneof("query"):
        case "select":
            new_dataset = do_select(query.select, dataset)
        case "filter":
            new_dataset = do_filters(query.filter, dataset)
        case "take":
            new_dataset = do_take(query.take, dataset)
        case "take_range":
            new_dataset = do_take_range(query.take_range, dataset)
        case "new_columns":
            new_dataset = do_with_new_columns(query.new_columns, dataset)

        case _:
            raise ValueError(f"Unimplemented query {query.WhichOneof('query')}")
    resp = DatasetSpecification(
        length=len(new_dataset), columns=new_dataset.columns, is_lightcone=False
    )
    return new_dataset, resp


def do_select(select_stmt: m.DatasetSelectStatement, dataset: oc.Dataset):
    result = dataset.select(select_stmt.columns)
    return result


def do_take(take_stmt: m.TakeStatement, dataset: oc.Dataset):
    at = str(take_stmt.TakeAt.Name(take_stmt.at)).lower()

    result = dataset.take(take_stmt.n, at=at)
    return result


def do_take_range(take_range):
    raise NotImplementedError


def do_with_new_columns(new_columns: WithNewColumnStatement, dataset: oc.Dataset):
    new_columns = {
        name: deserialize_derived_column(col)
        for name, col in new_columns.columns.items()
    }
    return dataset.with_new_columns(**new_columns)
