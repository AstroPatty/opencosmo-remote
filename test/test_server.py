import os
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from mpi4py import MPI

comm = MPI.COMM_WORLD


@pytest.fixture(scope="module")
def scratch_dir():
    if comm.Get_rank() == 0:
        path = mkdtemp()
    else:
        path = None

    tmp_directory = comm.bcast(path)
    os.environ["SCRATCH_PATH"] = tmp_directory
    # Any extra setup here

    yield Path(tmp_directory)

    rmtree(path)
