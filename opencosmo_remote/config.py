from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import Sequence

from mpi4py import MPI
from pydantic import Field
from pydantic_settings import BaseSettings

COMM = MPI.COMM_WORLD


def can_write(scratch_path: Path, comm):
    if scratch_path.is_file():
        raise ValueError("Scratch path must point to a directory!")

    if not scratch_path.exists():
        if comm.Get_rank() == 0:
            warnings.warn(
                "Expected an existing folder for the scratch path. "
                "opencosmo-remote will create a subfolder"
            )
        if os.access(scratch_path.parent, os.W_OK):
            return scratch_path

    if not os.access(scratch_path, os.W_OK):
        raise ValueError("Scratch path points so a read-only directory!")
    return scratch_path


def get_settings(comm: MPI.Comm, root: int, **kwargs):
    if comm.Get_rank() == root:
        SettingsCls = OpenCosmoRemotePointSettings
    else:
        SettingsCls = OpenCosmoRemoteFollowerSettings

    try:
        settings = SettingsCls(**kwargs)
        all_settings = comm.allgather(settings)
    except Exception as e:  # Catchall for graceful shutdown
        all_settings = comm.allgather(e)

    failures = list(filter(lambda s: isinstance(s, Exception), all_settings))
    if any(isinstance(s, Exception) for s in all_settings):
        raise ValueError(
            "At least one rank was unable to initialize due to bad settings. \n"
            f"Error: {failures[0]}"
        )
    verify_settings(all_settings, comm)
    return settings


SETTINGS = get_settings


def verify_settings(
    settings: Sequence[OpenCosmoRemotePointSettings | OpenCosmoRemoteFollowerSettings],
    comm,
):
    paths = set([s.scratch_path for s in settings])
    if len(paths) > 1:
        raise ValueError("All ranks must have the same scratch path!")
    path = can_write(paths.pop(), comm)
    if comm.Get_rank() == 0:
        path.mkdir(exist_ok=True)


class OpenCosmoRemotePointSettings(BaseSettings):
    port: int = Field(ge=49152, le=65535, default=50051)
    scratch_path: Path


class OpenCosmoRemoteFollowerSettings(BaseSettings):
    scratch_path: Path
