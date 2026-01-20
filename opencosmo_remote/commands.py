import opencosmo as oc

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages import Token
from opencosmo_remote.messages.open_pb2 import DataType, InternalOpenStatement
from opencosmo_remote.messages.query_pb2 import (
    DatasetSpecification,
    OpenCosmoDataSpecification,
    OutputPath,
    QueryResponse,
    StructureCollectionSpecification,
    WriteStatement,
)
from opencosmo_remote.paths import get_halo_paths


def handle_message(message, datasets, settings):
    """
    This is the main query handler. Currently has three cases:
    1. InternalOpenStatement - open a dataset
    2. Token - Close the dataset associated with the token
    3. All others - perform query
    """
    match message:
        case InternalOpenStatement():
            return open_dataset(message, datasets)
        case WriteStatement():
            path = write_data(message, datasets, settings)
            return datasets, path
        case Token():
            datasets.pop(message.uuid)
            return datasets, None
        case _:
            dataset = datasets[message.token.uuid]
            new_ds, response = execute_message(message, dataset)
            datasets[message.token.uuid] = new_ds
            return datasets, response


def write_data(message, datasets, settings):
    dataset = datasets[message.token.uuid]
    scratch_path = settings.scratch_path
    path = scratch_path / f"{message.token.uuid}.hdf5"
    i = 0
    while path.exists():
        path = scratch_path / f"{message.token.uuid}_{i}.hdf5"
        i += 1

    oc.write(path, dataset)
    return OutputPath(path=str(path))


def open_dataset(stmt: InternalOpenStatement, datasets: dict):
    dtypes = list(map(lambda i: DataType.Name(i), stmt.dtypes))
    paths = get_halo_paths(
        stmt.dataset_path, flatten=True, dtypes=dtypes, step_numbers=stmt.step_number
    )
    dataset = oc.open(*paths)
    if isinstance(dataset, oc.Dataset):
        spec_t = DatasetSpecification(
            length=len(dataset), columns=dataset.columns, is_lightcone=False
        )
        spec = OpenCosmoDataSpecification(ds=spec_t)
    elif isinstance(dataset, oc.StructureCollection):
        spec_t = StructureCollectionSpecification(
            length=len(dataset), datasets=list(dataset.keys())
        )
        spec = OpenCosmoDataSpecification(sc=spec_t)

    resp = QueryResponse(spec=spec, message="", new_token=Token(uuid=stmt.uuid))
    return datasets | {stmt.uuid: dataset}, resp
