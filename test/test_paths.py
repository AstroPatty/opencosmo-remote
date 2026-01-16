from pathlib import Path

import pytest

from opencosmo_remote.paths import get_halo_paths


@pytest.fixture
def data_root() -> Path:
    return Path(__file__).resolve().parents[1] / "test_data"


def test_get_halo_paths_flatten_default(data_root):
    paths = get_halo_paths(data_root, flatten=True)
    assert paths, "Expected at least one dataset path"
    assert all(path.exists() for path in paths)


def test_get_halo_paths_with_dtype_filter(data_root):
    paths = get_halo_paths(
        data_root, step_numbers=624, dtypes=["HALO_PROPERTIES"], flatten=True
    )
    assert paths, "Expected halo properties path for step_624"
    assert all(path.name.startswith("haloproperties") for path in paths)


def test_get_halo_paths_invalid_step(data_root):
    with pytest.raises(ValueError):
        get_halo_paths(data_root, step_numbers=999999, flatten=True)
