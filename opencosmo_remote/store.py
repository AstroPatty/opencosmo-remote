import dbm
from pathlib import Path
from typing import Any

from appdirs import user_data_dir


def __get_path():
    path = Path(user_data_dir()) / "opencosmo-remote"
    path.mkdir(parents=False, exist_ok=True)
    return path / "datasets.db"


def write(key: str, value: Any, overwrite=False):
    with dbm.open(__get_path(), "c") as db:
        if key in db and not overwrite:
            raise ValueError(f"Already have a registered dataset named {key}")
        db[key] = value


def read(key: str):
    with dbm.open(__get_path(), "r") as db:
        return db[key].decode()
