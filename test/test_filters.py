import opencosmo as oc
from opencosmo.column.column import ColumnMask

from opencosmo_remote.filters import deserialize_filters, serialize_filter
from opencosmo_remote.messages.filter_pb2 import FilterStatement


def compare_filters(f1: ColumnMask, f2: ColumnMask):
    assert f1.column_name == f2.column_name
    assert f1.operator == f2.operator
    assert f1.value == f2.value


def do_test(*masks: ColumnMask):
    serialized_masks = map(serialize_filter, masks)
    stmt = FilterStatement(filters=list(serialized_masks))
    deserialized_masks = deserialize_filters(stmt)
    for sm, dsm in zip(masks, deserialized_masks):
        compare_filters(sm, dsm)


def test_mask_with_float():
    mask = oc.col("mass") > 1.0
    do_test(mask)


def test_mask_with_int():
    mask = oc.col("mass") > 1
    do_test(mask)


def test_mask_gte():
    m1 = oc.col("mass") >= 2
    m2 = oc.col("mass2") >= 3
    do_test(m1, m2)


def test_mask_lt():
    m1 = oc.col("mass") < 2
    m2 = oc.col("mass2") < 3
    do_test(m1, m2)


def test_mask_lte():
    m1 = oc.col("mass") <= 2
    m2 = oc.col("mass2") <= 3
    do_test(m1, m2)


def test_mask_eq():
    m1 = oc.col("mass") == 2
    m2 = oc.col("mass2") == 3
    do_test(m1, m2)


def test_mask_neq():
    m1 = oc.col("mass") != 2
    m2 = oc.col("mass2") != 3
    do_test(m1, m2)


def test_mask_neg():
    m1 = oc.col("mass") > -2
    m2 = oc.col("mass2") < -3
    do_test(m1, m2)
