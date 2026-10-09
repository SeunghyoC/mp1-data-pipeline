# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)
    df = df.drop_duplicates()
    rows_after = len(df)
    logger.debug(
        f"remove_duplicates: {rows_before} → {rows_after} rows "
        f"(removed {rows_before - rows_after})"
    )
    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        rows_before = len(df)
        df = df.dropna()
        rows_after = len(df)
        logger.debug(
            f"handle_missing: {rows_before} → {rows_after} rows "
            f"(removed {rows_before - rows_after})"
        )
    elif axis == "columns":
        cols_before = df.shape[1]
        df = df.dropna(axis=1)
        cols_after = df.shape[1]
        logger.debug(
            f"handle_missing: {cols_before} → {cols_after} columns "
            f"(removed {cols_before - cols_after})"
        )
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column not found: {column}")
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            logger.warning(f"Column is not numeric: {column}")
            continue

        rows_before = len(df)

        if method == "iqr":
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
        else:
            mean = df[column].mean()
            std = df[column].std()
            lower = mean - threshold * std
            upper = mean + threshold * std

        df = df[(df[column] >= lower) & (df[column] <= upper)]

        logger.debug(
            f"{column}: method={method}, threshold={threshold}, "
            f"lower={lower}, upper={upper}, removed={rows_before - len(df)}"
        )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]

    if processing["remove_duplicates"]:
        df = remove_duplicates(df)

    if processing["missing"]["enabled"]:
        df = handle_missing(df, axis=processing["missing"]["axis"])

    if processing["outliers"]["enabled"]:
        df = remove_outliers(
            df,
            processing["outliers"]["columns"],
            processing["outliers"]["method"],
            processing["outliers"]["threshold"],
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }
