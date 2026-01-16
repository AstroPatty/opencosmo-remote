from pathlib import Path

import opencosmo as oc
import pytest

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages import OpenCosmoQueryStage, TakeStatement
from opencosmo_remote.messages.select_pb2 import DatasetSelectStatement


@pytest.fixture
def dataset_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "test_data"
        / "analysis"
        / "halos"
        / "step_624"
        / "haloproperties"
        / "haloproperties.hdf5"
    )


def test_execute_take_returns_expected_length(dataset_path):
    ds = oc.open(dataset_path)
    stmt = TakeStatement(n=5, at="RANDOM")
    query_stage = OpenCosmoQueryStage(take=stmt)
    new_dataset, spec = execute_message(query_stage, ds)
    assert len(new_dataset) == 5
    assert spec.length == 5


def test_execute_select_reduces_columns(dataset_path):
    ds = oc.open(dataset_path)
    first_column = ds.columns[0]
    select_stmt = DatasetSelectStatement(columns=[first_column])
    query_stage = OpenCosmoQueryStage(select=select_stmt)
    new_dataset, spec = execute_message(query_stage, ds)
    assert list(new_dataset.columns) == [first_column]
    assert list(spec.columns) == [first_column]
