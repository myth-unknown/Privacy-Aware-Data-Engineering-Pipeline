"""
Data cleaning operations.
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(
    df: pd.DataFrame, subset: list[str] | None = None, keep: str = "first"
) -> pd.DataFrame:
    """
    Remove duplicate rows from DataFrame.

    Args:
        df: DataFrame to clean
        subset: Column names to consider for duplicates (None = all columns)
        keep: Which duplicates to keep ('first', 'last', False to drop all)

    Returns:
        DataFrame with duplicates removed
    """
    original_count = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    removed = original_count - len(df_clean)

    logger.info(f"Removed {removed} duplicate rows ({removed/original_count*100:.1f}%)")

    return df_clean


def fill_missing_values(
    df: pd.DataFrame,
    strategy: str = "drop",
    fill_value: any = None,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Fill or remove missing values.

    Args:
        df: DataFrame to clean
        strategy: 'drop', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill', 'constant'
        fill_value: Value to use for 'constant' strategy
        columns: Specific columns to apply to (None = all columns)

    Returns:
        DataFrame with missing values handled
    """
    df_clean = df.copy()
    target_cols = columns if columns else df_clean.columns.tolist()

    if strategy == "drop":
        df_clean = df_clean.dropna(subset=target_cols)
        logger.info(f"Dropped rows with missing values: {len(df) - len(df_clean)} rows removed")

    elif strategy == "mean":
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
        logger.info(f"Filled missing values with mean for {len(target_cols)} columns")

    elif strategy == "median":
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        logger.info(f"Filled missing values with median for {len(target_cols)} columns")

    elif strategy == "mode":
        for col in target_cols:
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
        logger.info(f"Filled missing values with mode for {len(target_cols)} columns")

    elif strategy == "forward_fill":
        df_clean[target_cols] = df_clean[target_cols].fillna(method="ffill")
        logger.info(f"Forward filled missing values for {len(target_cols)} columns")

    elif strategy == "backward_fill":
        df_clean[target_cols] = df_clean[target_cols].fillna(method="bfill")
        logger.info(f"Backward filled missing values for {len(target_cols)} columns")

    elif strategy == "constant":
        if fill_value is None:
            raise ValueError("fill_value must be provided for 'constant' strategy")
        df_clean[target_cols] = df_clean[target_cols].fillna(fill_value)
        logger.info(f"Filled missing values with constant '{fill_value}' for {len(target_cols)} columns")

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df_clean


def remove_outliers(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    method: str = "iqr",
    threshold: float = 1.5,
) -> pd.DataFrame:
    """
    Remove outliers from numeric columns.

    Args:
        df: DataFrame to clean
        columns: Numeric columns to check (None = all numeric columns)
        method: 'iqr' (interquartile range) or 'zscore' (standard deviation)
        threshold: IQR multiplier (1.5 = standard) or z-score threshold (3.0 = standard)

    Returns:
        DataFrame with outliers removed
    """
    df_clean = df.copy()

    # Get numeric columns
    if columns is None:
        columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    else:
        columns = [col for col in columns if pd.api.types.is_numeric_dtype(df_clean[col])]

    if not columns:
        logger.warning("No numeric columns found for outlier removal")
        return df_clean

    mask = pd.Series([True] * len(df_clean), index=df_clean.index)

    for col in columns:
        if method == "iqr":
            q1 = df_clean[col].quantile(0.25)
            q3 = df_clean[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            col_mask = (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)

        elif method == "zscore":
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            if std > 0:
                z_scores = np.abs((df_clean[col] - mean) / std)
                col_mask = z_scores <= threshold
            else:
                col_mask = pd.Series([True] * len(df_clean), index=df_clean.index)

        else:
            raise ValueError(f"Unknown method: {method}")

        mask = mask & col_mask

    df_clean = df_clean[mask]
    removed = len(df) - len(df_clean)

    logger.info(
        f"Removed {removed} outlier rows ({removed/len(df)*100:.1f}%) using {method} method"
    )

    return df_clean


def standardize_column_names(df: pd.DataFrame, style: str = "snake_case") -> pd.DataFrame:
    """
    Standardize column names to a consistent format.

    Args:
        df: DataFrame to clean
        style: 'snake_case', 'camelCase', 'PascalCase', or 'lowercase'

    Returns:
        DataFrame with standardized column names
    """
    df_clean = df.copy()

    if style == "snake_case":
        df_clean.columns = [
            col.strip().lower().replace(" ", "_").replace("-", "_")
            for col in df_clean.columns
        ]
    elif style == "lowercase":
        df_clean.columns = [col.strip().lower() for col in df_clean.columns]
    elif style == "camelCase":
        df_clean.columns = [
            _to_camel_case(col.strip()) for col in df_clean.columns
        ]
    elif style == "PascalCase":
        df_clean.columns = [
            _to_pascal_case(col.strip()) for col in df_clean.columns
        ]
    else:
        raise ValueError(f"Unknown style: {style}")

    logger.info(f"Standardized column names to {style}")

    return df_clean


def _to_camel_case(text: str) -> str:
    """Convert text to camelCase."""
    words = text.replace("_", " ").replace("-", " ").split()
    if not words:
        return text
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def _to_pascal_case(text: str) -> str:
    """Convert text to PascalCase."""
    words = text.replace("_", " ").replace("-", " ").split()
    return "".join(word.capitalize() for word in words)
