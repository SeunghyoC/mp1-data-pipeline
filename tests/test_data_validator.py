# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    # TODO: Set the required and numeric column names.
    required_columns = ["record_id", "name", "rating", "category", "status"]
    numeric_columns = ["rating"]
    # TODO: Call validate_dataframe().
    result = validate_dataframe(sample_df, required_columns, numeric_columns)
    # TODO: Assert that 98 rows remain and all five columns are preserved.
    assert len(result) == 98
    assert list(result.columns) == required_columns


def test_validate_dataframe_with_missing_column(sample_df):
    # TODO: Set required_columns to include a nonexistent column.
    required_columns = ["record_id", "name", "rating", "category", "status", "fake_column"]
    numeric_columns = ["rating"]
    # TODO: Use pytest.raises(ValueError) around validate_dataframe().
    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)
