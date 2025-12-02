import opencosmo as oc

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages.open_pb2 import DataType, InternalOpenStatement
from opencosmo_remote.paths import get_halo_paths


def handle_message(message, datasets):
    match message:
        case InternalOpenStatement():
            return open_dataset(message, datasets)
        case _:
            dataset = datasets[message.token.uuid]
            return execute_message(message, dataset)


def open_dataset(stmt: InternalOpenStatement, datasets: dict):
    dtypes = list(map(lambda i: DataType.Name(i), stmt.dtypes))
    paths = get_halo_paths(stmt.dataset_path, flatten=True, dtypes=dtypes)
    dataset = oc.open(*paths)
    return datasets | {stmt.uuid: dataset}
