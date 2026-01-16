import opencosmo as oc

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages import Token
from opencosmo_remote.messages.open_pb2 import DataType, InternalOpenStatement
from opencosmo_remote.messages.query_pb2 import DatasetSpecification, QueryResponse
from opencosmo_remote.paths import get_halo_paths


def handle_message(message, datasets):
    """
    This is the main query handler. Currently has three cases:
    1. InternalOpenStatement - open a dataset
    2. Token - Close the dataset associated with the token
    3. All others - perform query
    """
    match message:
        case InternalOpenStatement():
            return open_dataset(message, datasets)
        case Token():
            datasets.pop(message.uuid)
            return datasets, None
        case _:
            dataset = datasets[message.token.uuid]
            new_ds, response = execute_message(message, dataset)
            datasets[message.token.uuid] = new_ds
            return datasets, response


def open_dataset(stmt: InternalOpenStatement, datasets: dict):
    dtypes = list(map(lambda i: DataType.Name(i), stmt.dtypes))
    paths = get_halo_paths(stmt.dataset_path, flatten=True, dtypes=dtypes)
    dataset = oc.open(*paths)
    spec = DatasetSpecification(
        length=len(dataset), columns=dataset.columns, is_lightcone=False
    )
    resp = QueryResponse(spec=spec, message="", new_token=Token(uuid=stmt.uuid))
    return datasets | {stmt.uuid: dataset}, resp
