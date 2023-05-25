import sys
import pytest
from hypothesis import assume, given, settings
from hypothesis.extra.pandas import column, data_frames, range_indexes
import hypothesis.strategies as st
import numpy as np
from pandas import DataFrame
from pandas.testing import assert_frame_equal
import pandas as pd

from arcticc.version_store.processing import QueryBuilder
from arcticc.util.test import get_wide_dataframe, make_dynamic, regularize_dataframe
from arcticc.util.hypothesis import integral_type_strategies, numeric_type_strategies, string_strategy


def generic_dynamic_filter_test(version_store, symbol, df, arctic_query, pandas_query):
    expected, slices = make_dynamic(df)
    for df_slice in slices:
        version_store.append(symbol, df_slice, write_if_missing=True)

    try:
        expected = expected.query(pandas_query)
        received = version_store.read(symbol, query_builder=arctic_query).data
        expected = regularize_dataframe(expected)
        received = regularize_dataframe(received)
        if not len(expected) == 0 and len(received) == 0:
            if not np.array_equal(expected, received):
                print("Original dataframe\n{}".format(expected))
                print("Pandas query\n{}".format(pandas_query))
                print("Expected\n{}".format(expected))
                print("Received\n{}".format(received))
                assert False
    except pd.core.computation.ops.UndefinedVariableError:
        # Might have edited out the query columns entirely
        pass

    assert True


@settings(deadline=None)
@given(
    df=data_frames(
        [
            column("a", elements=numeric_type_strategies()),
            column("b", elements=numeric_type_strategies()),
            column("c", elements=numeric_type_strategies()),
            column("d", elements=string_strategy),
        ],
        index=range_indexes(),
    )
)
def test_filter_less_than_col_col(lmdb_version_store_dynamic_schema, df):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"] < q["b"]]
    pandas_query = "a < b"
    generic_dynamic_filter_test(lmdb_version_store_dynamic_schema, "test_filter_less_than_col_col", df, q, pandas_query)


@settings(deadline=None)
@given(
    df=data_frames(
        [
            column("a", elements=numeric_type_strategies()),
            column("b", elements=numeric_type_strategies()),
            column("c", elements=numeric_type_strategies()),
            column("d", elements=string_strategy),
        ],
        index=range_indexes(),
    ),
    val=numeric_type_strategies(),
)
def test_filter_less_than_equals_col_val(lmdb_version_store_dynamic_schema, df, val):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"] <= val]
    pandas_query = "a <= {}".format(val)
    generic_dynamic_filter_test(
        lmdb_version_store_dynamic_schema, "test_filter_less_than_equals_col_val", df, q, pandas_query
    )


@settings(deadline=None)
@given(
    df=data_frames(
        [
            column("a", elements=numeric_type_strategies()),
            column("b", elements=numeric_type_strategies()),
            column("c", elements=numeric_type_strategies()),
            column("d", elements=string_strategy),
        ],
        index=range_indexes(),
    ),
    val=numeric_type_strategies(),
)
def test_filter_less_than_equals_val_col(lmdb_version_store_dynamic_schema, df, val):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[val <= q["a"]]
    pandas_query = "{} <= a".format(val)
    generic_dynamic_filter_test(
        lmdb_version_store_dynamic_schema, "test_filter_less_than_equals_val_col", df, q, pandas_query
    )


@settings(deadline=None)
@given(
    df=data_frames(
        [
            column("a", elements=numeric_type_strategies()),
            column("b", elements=numeric_type_strategies()),
            column("c", elements=numeric_type_strategies()),
            column("d", elements=string_strategy),
        ],
        index=range_indexes(),
    )
)
def test_filter_less_than_equals_col_col(lmdb_version_store_dynamic_schema, df):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"] <= q["b"]]
    pandas_query = "a <= b"
    generic_dynamic_filter_test(
        lmdb_version_store_dynamic_schema, "test_filter_less_than_equals_col_col", df, q, pandas_query
    )


@pytest.mark.skipif(sys.platform == "win32", reason="SKIP_WIN Issues with numeric filters")
@settings(deadline=None)
@given(
    df=data_frames(
        [
            column("a", elements=numeric_type_strategies()),
            column("b", elements=numeric_type_strategies()),
            column("c", elements=numeric_type_strategies()),
            column("d", elements=string_strategy),
        ],
        index=range_indexes(),
    ),
    val=numeric_type_strategies(),
)
def test_filter_greater_than_col_val(lmdb_version_store_dynamic_schema, df, val):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"] > val]
    pandas_query = "a > {}".format(val)
    generic_dynamic_filter_test(
        lmdb_version_store_dynamic_schema, "test_filter_greater_than_col_val", df, q, pandas_query
    )


@settings(deadline=None)
@given(
    df=data_frames(
        [column("a", elements=string_strategy), column("b", elements=string_strategy)], index=range_indexes()
    ),
    vals=st.frozensets(string_strategy, min_size=1),
)
def test_filter_string_isin(lmdb_version_store_dynamic_schema, df, vals):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"].isin(vals)]
    pandas_query = "a in {}".format(list(vals))
    generic_dynamic_filter_test(lmdb_version_store_dynamic_schema, "test_filter_string_isin", df, q, pandas_query)


@settings(deadline=None)
@given(
    df=data_frames(
        [column("a", elements=string_strategy), column("b", elements=string_strategy)], index=range_indexes()
    )
)
def test_filter_string_isin_empty_set(lmdb_version_store_dynamic_schema, df):
    assume(not df.empty)
    vals = []
    q = QueryBuilder()
    q = q[q["a"].isin(vals)]
    pandas_query = "a in {}".format(list(vals))
    generic_dynamic_filter_test(
        lmdb_version_store_dynamic_schema, "test_filter_string_isin_empty_set", df, q, pandas_query
    )


@settings(deadline=None)
@given(
    df=data_frames(
        [column("a", elements=string_strategy), column("b", elements=string_strategy)], index=range_indexes()
    ),
    vals=st.frozensets(string_strategy, min_size=1),
)
def test_filter_string_isnotin(lmdb_version_store_dynamic_schema, df, vals):
    assume(not df.empty)
    q = QueryBuilder()
    q = q[q["a"].isnotin(vals)]
    pandas_query = "a not in {}".format(list(vals))
    generic_dynamic_filter_test(lmdb_version_store_dynamic_schema, "test_filter_string_isnotin", df, q, pandas_query)


def test_numeric_filter_dynamic_schema(lmdb_version_store_tiny_segment_dynamic):
    symbol = "test_numeric_filter_dynamic_schema"
    lib = lmdb_version_store_tiny_segment_dynamic
    df = get_wide_dataframe(100)
    expected, slices = make_dynamic(df)
    for df_slice in slices:
        lib.append(symbol, df_slice, write_if_missing=True)
    val = 0
    q = QueryBuilder()
    q = q[q["int8"] < val]
    pandas_query = "int8 < {}".format(val)
    expected = expected.query(pandas_query)
    received = lib.read(symbol, query_builder=q).data
    expected = regularize_dataframe(expected)
    received = regularize_dataframe(received)
    assert_frame_equal(expected, received)


@pytest.mark.skipif(sys.platform == "win32", reason="SKIP_WIN dtype is int32 on vit.data")
def test_filter_column_not_present_dynamic(lmdb_version_store_dynamic_schema):
    df = DataFrame({"a": np.arange(2)}, index=np.arange(2))
    q = QueryBuilder()
    q = q[q["b"] < 5]
    symbol = "test_filter_column_not_present_static"
    lmdb_version_store_dynamic_schema.write(symbol, df)
    vit = lmdb_version_store_dynamic_schema.read(symbol, query_builder=q)
    expected = pd.DataFrame({"a": pd.Series(dtype="int64")}, index=pd.Int64Index([], dtype="int64"))
    assert_frame_equal(vit.data, expected)


def test_filter_column_type_change(lmdb_version_store_dynamic_schema):
    lib = lmdb_version_store_dynamic_schema
    symbol = "test_filter_column_type_change"

    # Write a column of float type
    df1 = pd.DataFrame({"col": [0.0]}, index=pd.date_range("2000-01-01", periods=1))
    lib.write(symbol, df1)
    # Append a column of int type
    df2 = pd.DataFrame({"col": [np.uint8(1)]}, index=pd.date_range("2000-01-02", periods=1))
    lib.append(symbol, df2)

    q = QueryBuilder()
    q = q[q["col"] == 1]
    received = lib.read(symbol, query_builder=q).data
    expected = df1.append(df2).query("col == 1")
    assert np.array_equal(expected, received)

    # Fixed width strings, width 1
    df1 = pd.DataFrame({"col": ["a", "b"]}, index=pd.date_range("2000-01-01", periods=2))
    lib.write(symbol, df1, dynamic_strings=False)
    # Fixed width strings, width 2
    df2 = pd.DataFrame({"col": ["a", "bb"]}, index=pd.date_range("2000-01-03", periods=2))
    lib.append(symbol, df2, dynamic_strings=False)
    # Dynamic strings
    df3 = pd.DataFrame({"col": ["a", "bbb"]}, index=pd.date_range("2000-01-05", periods=2))
    lib.append(symbol, df3, dynamic_strings=True)

    q = QueryBuilder()
    q = q[q["col"] == "a"]
    received = lib.read(symbol, query_builder=q).data
    expected = df1.append(df2).append(df3).query("col == 'a'")
    assert np.array_equal(expected, received)
