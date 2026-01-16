import opencosmo as oc

from opencosmo_remote.execute import execute_message
from opencosmo_remote.messages import OpenCosmoQueryStage, TakeStatement

DATA_SOURCE = (
    "/Users/patrick/code/prod/OpenCosmo/test_data/snapshot/haloproperties.hdf5"
)


def test_take_statement():
    stmt = TakeStatement(n=100, at="RANDOM")
    query_stage = OpenCosmoQueryStage(take=stmt)
    ds = oc.open(DATA_SOURCE)
    dataset, resp = execute_message(query_stage, ds)
    assert len(dataset) == 100
