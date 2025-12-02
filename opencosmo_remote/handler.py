from pathlib import Path
from typing import Optional

import opencosmo as oc

from opencosmo_remote.paths import get_halo_paths


def create_query_handler(
    base_path: Path, step: int, data_types: Optional[str | list[str]]
):
    paths = get_halo_paths(base_path, step, data_types, flatten=True)
    return QueryHandler.from_paths(paths)


class QueryHandler:
    def __init__(
        self,
        dataset: oc.Dataset | oc.StructureCollection,
    ):
        self.datasets = {}

    @classmethod
    def from_paths(cls, paths: list[Path]):
        ds = oc.open(*paths)
        return QueryHandler(dataset=ds)
