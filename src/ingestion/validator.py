"""
Validation utilities for uploaded files and DataFrames.
"""

import logging
from pathlib import Path

import pandas as pd

from src.ingestion.models import IngestionResult, IssueSeverity

logger = logging.getLogger(__name__)

# Default constraints
DEFAULT_MAX_FILE_SIZE_MB = 100
DEFAULT_MAX_ROWS = 1_000_000
DEFAULT_MAX_COLUMNS = 1000
DEFAULT_ALLOWED_EXTENSIONS = [".csv", ".json"]


def validate_file(
    file_path: str | Path,
    max_size_mb: float = DEFAULT_MAX_FILE_SIZE_MB,
    allowed_extensions: list[str] | None = None,
) -> IngestionResult:
    """
    Validate file before loading (size, extension, existence).

    Args:
        file_path: Path to file
        max_size_mb: Maximum allowed file size in MB
        allowed_extensions: List of allowed file extensions (e.g., ['.csv', '.json'])

    Returns:
        IngestionResult with validation issues
    """
    file_path = Path(file_path)
    result = IngestionResult(success=True, file_name=file_path.name)

    if allowed_extensions is None:
        allowed_extensions = DEFAULT_ALLOWED_EXTENSIONS

    # Check file existence
    if not file_path.exists():
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"File not found: {file_path}",
        )
        return result

    # Check file extension
    file_ext = file_path.suffix.lower()
    if file_ext not in allowed_extensions:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"Invalid file type: {file_ext}. Allowed: {', '.join(allowed_extensions)}",
        )

    # Check file size
    file_size_bytes = file_path.stat().st_size
    file_size_mb = file_size_bytes / (1024 * 1024)
    result.file_size_bytes = file_size_bytes

    if file_size_mb > max_size_mb:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"File too large: {file_size_mb:.2f} MB (max: {max_size_mb} MB)",
        )
    elif file_size_mb > max_size_mb * 0.8:
        result.add_issue(
            IssueSeverity.WARNING,
            f"Large file: {file_size_mb:.2f} MB (approaching limit of {max_size_mb} MB)",
        )

    # Check if file is empty
    if file_size_bytes == 0:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            "File is empty",
        )

    logger.info(
        f"File validation: {file_path.name} - "
        f"{'PASS' if result.success else 'FAIL'} "
        f"({len(result.issues)} issues)"
    )

    return result


def validate_dataframe(
    df: pd.DataFrame,
    file_name: str = "uploaded_file",
    max_rows: int = DEFAULT_MAX_ROWS,
    max_columns: int = DEFAULT_MAX_COLUMNS,
    min_rows: int = 1,
    min_columns: int = 1,
) -> IngestionResult:
    """
    Validate DataFrame after loading (shape, nulls, duplicates).

    Args:
        df: Loaded DataFrame
        file_name: Original file name for reporting
        max_rows: Maximum allowed number of rows
        max_columns: Maximum allowed number of columns
        min_rows: Minimum required number of rows
        min_columns: Minimum required number of columns

    Returns:
        IngestionResult with validation issues and metadata
    """
    result = IngestionResult(
        success=True,
        data=df,
        file_name=file_name,
        num_rows=len(df),
        num_columns=len(df.columns),
        column_names=df.columns.tolist(),
    )

    # Check minimum requirements
    if len(df) < min_rows:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"Insufficient rows: {len(df)} (minimum: {min_rows})",
        )

    if len(df.columns) < min_columns:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"Insufficient columns: {len(df.columns)} (minimum: {min_columns})",
        )

    # Check maximum limits
    if len(df) > max_rows:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"Too many rows: {len(df):,} (max: {max_rows:,})",
        )

    if len(df.columns) > max_columns:
        result.success = False
        result.add_issue(
            IssueSeverity.ERROR,
            f"Too many columns: {len(df.columns)} (max: {max_columns})",
        )

    # Warn about empty DataFrame
    if df.empty:
        result.add_issue(
            IssueSeverity.WARNING,
            "DataFrame is empty (no rows)",
        )

    # Check for unnamed columns
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed:")]
    if unnamed_cols:
        result.add_issue(
            IssueSeverity.WARNING,
            f"Found {len(unnamed_cols)} unnamed column(s): {unnamed_cols[:3]}",
            details={"unnamed_columns": unnamed_cols},
        )

    # Check for duplicate column names
    duplicate_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicate_cols:
        result.add_issue(
            IssueSeverity.WARNING,
            f"Duplicate column names detected: {duplicate_cols[:5]}",
            details={"duplicate_columns": duplicate_cols},
        )

    # Check for missing values
    total_nulls = df.isnull().sum().sum()
    if total_nulls > 0:
        null_pct = (total_nulls / (len(df) * len(df.columns))) * 100
        columns_with_nulls = df.columns[df.isnull().any()].tolist()

        severity = IssueSeverity.WARNING if null_pct < 50 else IssueSeverity.ERROR
        if null_pct >= 50:
            result.success = False

        result.add_issue(
            severity,
            f"Missing values detected: {total_nulls:,} ({null_pct:.1f}%)",
            details={
                "total_nulls": int(total_nulls),
                "null_percentage": round(null_pct, 2),
                "columns_with_nulls": columns_with_nulls,
            },
        )

    # Check for fully null columns
    fully_null_cols = df.columns[df.isnull().all()].tolist()
    if fully_null_cols:
        result.add_issue(
            IssueSeverity.WARNING,
            f"Columns with all null values: {fully_null_cols[:5]}",
            details={"fully_null_columns": fully_null_cols},
        )

    # Check for duplicate rows
    num_duplicates = df.duplicated().sum()
    if num_duplicates > 0:
        dup_pct = (num_duplicates / len(df)) * 100
        result.add_issue(
            IssueSeverity.INFO,
            f"Duplicate rows detected: {num_duplicates:,} ({dup_pct:.1f}%)",
            details={
                "num_duplicates": int(num_duplicates),
                "duplicate_percentage": round(dup_pct, 2),
            },
        )

    # Add metadata
    result.metadata["dtypes"] = df.dtypes.astype(str).to_dict()
    result.metadata["memory_usage_bytes"] = int(df.memory_usage(deep=True).sum())

    logger.info(
        f"DataFrame validation: {file_name} - "
        f"{'PASS' if result.success else 'FAIL'} "
        f"({len(result.issues)} issues)"
    )

    return result
