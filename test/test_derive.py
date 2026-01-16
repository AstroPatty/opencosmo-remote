import opencosmo as oc
from opencosmo.column import norm_cols
from opencosmo.column.column import Column, DerivedColumn

from opencosmo_remote.columns import (
    deserialize_derived_column,
    serialize_derived_column,
)


def compare_derived(d1: DerivedColumn, d2: DerivedColumn):
    # There is one possible difference. Ints are always promoted to floats for
    # Serialization purposes
    if isinstance(d1.lhs, int):
        assert isinstance(d2.lhs, (int, float))
    else:
        assert type(d1.lhs) is type(d2.lhs)
    if isinstance(d1.rhs, int):
        assert isinstance(d2.rhs, (int, float))
    else:
        assert type(d1.rhs) is type(d2.rhs)

    match d1.lhs:
        case DerivedColumn():
            compare_derived(d1.lhs, d2.lhs)
        case Column():
            assert d1.lhs.column_name == d2.lhs.column_name
        case _:
            assert d1.lhs == d2.lhs
    match d1.rhs:
        case DerivedColumn():
            compare_derived(d1.rhs, d2.rhs)
        case Column():
            assert d1.rhs.column_name == d2.rhs.column_name
        case _:
            assert d1.rhs == d2.rhs
    assert d1.operation == d2.operation


def do_test(column: DerivedColumn):
    serialized = serialize_derived_column(column)
    deserialized = deserialize_derived_column(serialized)
    compare_derived(column, deserialized)


def test_derived_from_existing_multiply():
    dc = oc.col("column_a") * oc.col("column_b")
    do_test(dc)


def test_derived_from_existing_divide():
    dc = oc.col("column_a") / oc.col("column_b")
    do_test(dc)


def test_derived_from_existing_add():
    dc = oc.col("column_a") + oc.col("column_b")
    do_test(dc)


def test_derived_from_existing_subtract():
    dc = oc.col("column_a") - oc.col("column_b")
    do_test(dc)


def test_derived_from_scalar_multiply():
    dc1 = 5.3 * oc.col("column_b")
    dc2 = 5 * oc.col("column_b")
    do_test(dc1)
    do_test(dc2)


def test_derived_from_scalar_divide():
    dc1 = 5.3 / oc.col("column_b")
    dc2 = 5 / oc.col("column_b")
    do_test(dc1)
    do_test(dc2)


def test_nested_derived_multiply():
    dc1 = oc.col("column_a") * oc.col("column_b")
    dc2 = dc1 * oc.col("column_b")
    do_test(dc2)


def test_nested_derived_divide():
    dc1 = oc.col("column_a") * oc.col("column_b")
    dc2 = dc1 / oc.col("column_b")
    do_test(dc2)


def test_nested_derived_add():
    dc1 = oc.col("column_a") + oc.col("column_b")
    dc2 = dc1 + oc.col("column_b")
    do_test(dc2)


def test_add_squared():
    dc1 = oc.col("column_a") ** 2
    dc2 = oc.col("column_b") ** 2
    dc3 = dc1 + dc2
    do_test(dc3.sqrt())


def test_norm_cols():
    dc = norm_cols("vx", "vy", "vz")
    do_test(dc)
