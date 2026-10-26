"""
Data quality profiling utilities.
"""

import logging

import pandas as pd

from src.validation.models import ColumnProfile, QualityIssue, QualityProfile

logger = logging.getLogger(__name__)

# Thresholds for quality scoring
NULL_THRESHOLD_HIGH = 0.5  # >50% nulls = high severity
NULL_THRESHOLD_MEDIUM = 0.2  # >20% nulls = medium severity
DUPLICATE_THRESHOLD_HIGH = 0.3  # >30% duplicates = high severity
DUPLICATE_THRESHOLD_MEDIUM = 0.1  # >10% duplicates = medium severity


def profile_dataframe(df: pd.DataFrame) -> QualityProfile:
    """
    Generate comprehensive quality profile for a DataFrame.

    Args:
        df: DataFrame to profile

    Returns:
        QualityProfile with statistics and issues
    """
    logger.info(f"Profiling DataFrame: {len(df)} rows, {len(df.columns)} columns")

    profile = QualityProfile(
        num_rows=len(df),
        num_columns=len(df.columns),
        memory_usage_bytes=int(df.memory_usage(deep=True).sum()),
    )

    # Overall statistics
    profile.total_nulls = int(df.isnull().sum().sum())
    profile.null_percentage = (
        profile.total_nulls / (len(df) * len(df.columns)) * 100
        if len(df) > 0 and len(df.columns) > 0
        else 0.0
    )
    profile.duplicate_rows = int(df.duplicated().sum())
    profile.duplicate_percentage = (
        profile.duplicate_rows / len(df) * 100 if len(df) > 0 else 0.0
    )

    # Categorize columns by type
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        if pd.api.types.is_bool_dtype(df[col]):
            profile.boolean_columns.append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            profile.numeric_columns.append(col)
        elif pd.api.types.is_string_dtype(df[col]) or dtype_str in ["object", "str"]:
            profile.string_columns.append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            profile.datetime_columns.append(col)

    # Profile each column
    for col in df.columns:
        col_profile = _profile_column(df[col])
        profile.column_profiles[col] = col_profile

    # Detect issues
    _detect_quality_issues(df, profile)

    # Calculate quality score
    profile.quality_score = _calculate_quality_score(profile)

    logger.info(
        f"Profiling complete: quality_score={profile.quality_score:.1f}, "
        f"issues={len(profile.issues)}"
    )

    return profile


def _profile_column(series: pd.Series) -> ColumnProfile:
    """Profile a single column."""
    col_profile = ColumnProfile(
        name=series.name,
        dtype=str(series.dtype),
        non_null_count=int(series.notna().sum()),
        null_count=int(series.isna().sum()),
        null_percentage=(series.isna().sum() / len(series) * 100) if len(series) > 0 else 0.0,
        unique_count=int(series.nunique()),
        duplicate_count=int((series.notna() & series.duplicated()).sum()),
    )

        # Numeric statistics
    if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
        non_null = series.dropna()
        if len(non_null) > 0:
            col_profile.mean = float(non_null.mean())
            col_profile.median = float(non_null.median())
            col_profile.std = float(non_null.std()) if len(non_null) > 1 else 0.0
            col_profile.min_value = float(non_null.min())
            col_profile.max_value = float(non_null.max())
            col_profile.q25 = float(non_null.quantile(0.25))
            col_profile.q75 = float(non_null.quantile(0.75))

    # String statistics
    elif pd.api.types.is_string_dtype(series) or str(series.dtype) == "object":
        non_null = series.dropna()
        if len(non_null) > 0:
            lengths = non_null.astype(str).str.len()
            col_profile.min_length = int(lengths.min())
            col_profile.max_length = int(lengths.max())
            col_profile.avg_length = float(lengths.mean())

    # Top values (limit to 10)
    value_counts = series.value_counts().head(10)
    col_profile.top_values = {str(k): int(v) for k, v in value_counts.items()}

    return col_profile


def _detect_quality_issues(df: pd.DataFrame, profile: QualityProfile) -> None:
    """Detect quality issues and add them to profile."""

    # Overall null percentage issue
    if profile.null_percentage > NULL_THRESHOLD_HIGH * 100:
        profile.add_issue(
            QualityIssue(
                column="[ALL]",
                issue_type="missing_values",
                severity="high",
                count=profile.total_nulls,
                percentage=profile.null_percentage,
                description=f"High percentage of missing values across dataset ({profile.null_percentage:.1f}%)",
            )
        )
    elif profile.null_percentage > NULL_THRESHOLD_MEDIUM * 100:
        profile.add_issue(
            QualityIssue(
                column="[ALL]",
                issue_type="missing_values",
                severity="medium",
                count=profile.total_nulls,
                percentage=profile.null_percentage,
                description=f"Moderate missing values across dataset ({profile.null_percentage:.1f}%)",
            )
        )

    # Duplicate rows issue
    if profile.duplicate_percentage > DUPLICATE_THRESHOLD_HIGH * 100:
        profile.add_issue(
            QualityIssue(
                column="[ALL]",
                issue_type="duplicates",
                severity="high",
                count=profile.duplicate_rows,
                percentage=profile.duplicate_percentage,
                description=f"High percentage of duplicate rows ({profile.duplicate_percentage:.1f}%)",
            )
        )
    elif profile.duplicate_percentage > DUPLICATE_THRESHOLD_MEDIUM * 100:
        profile.add_issue(
            QualityIssue(
                column="[ALL]",
                issue_type="duplicates",
                severity="medium",
                count=profile.duplicate_rows,
                percentage=profile.duplicate_percentage,
                description=f"Moderate duplicate rows ({profile.duplicate_percentage:.1f}%)",
            )
        )

    # Column-specific issues
    for col_name, col_profile in profile.column_profiles.items():
        # High null percentage in column
        if col_profile.null_percentage > NULL_THRESHOLD_HIGH * 100:
            profile.add_issue(
                QualityIssue(
                    column=col_name,
                    issue_type="missing_values",
                    severity="high",
                    count=col_profile.null_count,
                    percentage=col_profile.null_percentage,
                    description=f"Column '{col_name}' has {col_profile.null_percentage:.1f}% missing values",
                )
            )
        elif col_profile.null_percentage > NULL_THRESHOLD_MEDIUM * 100:
            profile.add_issue(
                QualityIssue(
                    column=col_name,
                    issue_type="missing_values",
                    severity="medium",
                    count=col_profile.null_count,
                    percentage=col_profile.null_percentage,
                    description=f"Column '{col_name}' has {col_profile.null_percentage:.1f}% missing values",
                )
            )

        # Low cardinality (potentially constant column)
        if col_profile.unique_count == 1 and col_profile.non_null_count > 0:
            profile.add_issue(
                QualityIssue(
                    column=col_name,
                    issue_type="low_cardinality",
                    severity="low",
                    count=1,
                    percentage=0.0,
                    description=f"Column '{col_name}' has only 1 unique value (constant column)",
                )
            )


def _calculate_quality_score(profile: QualityProfile) -> float:
    """
    Calculate overall quality score (0-100).

    Scoring factors:
    - Completeness (no nulls): 40 points
    - Uniqueness (no duplicates): 30 points
    - Consistency (no high severity issues): 20 points
    - Validity (no medium severity issues): 10 points
    """
    score = 100.0

    # Completeness penalty (max -40)
    completeness_penalty = min(40, profile.null_percentage * 0.8)
    score -= completeness_penalty

    # Uniqueness penalty (max -30)
    uniqueness_penalty = min(30, profile.duplicate_percentage * 1.0)
    score -= uniqueness_penalty

    # Issue penalties
    high_issue_penalty = len(profile.high_severity_issues) * 10
    medium_issue_penalty = len(profile.medium_severity_issues) * 5
    score -= min(20, high_issue_penalty)
    score -= min(10, medium_issue_penalty)

    return max(0.0, score)
