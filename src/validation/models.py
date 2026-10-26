"""
Data models for validation module.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QualityIssue:
    """Represents a data quality issue."""

    column: str
    issue_type: str  # e.g., "missing_values", "duplicates", "outliers"
    severity: str  # "low", "medium", "high"
    count: int
    percentage: float
    description: str
    details: dict[str, any] = field(default_factory=dict)


@dataclass
class ColumnProfile:
    """Statistical profile for a single column."""

    name: str
    dtype: str
    non_null_count: int
    null_count: int
    null_percentage: float
    unique_count: int
    duplicate_count: int

    # Numeric statistics (None for non-numeric)
    mean: float | None = None
    median: float | None = None
    std: float | None = None
    min_value: float | None = None
    max_value: float | None = None
    q25: float | None = None
    q75: float | None = None

    # String statistics (None for non-string)
    min_length: int | None = None
    max_length: int | None = None
    avg_length: float | None = None

    # Top values
    top_values: dict[str, int] = field(default_factory=dict)


@dataclass
class QualityProfile:
    """Overall data quality profile for a DataFrame."""

    # Basic metadata
    num_rows: int
    num_columns: int
    memory_usage_bytes: int
    profile_timestamp: datetime = field(default_factory=datetime.now)

    # Quality metrics
    total_nulls: int = 0
    null_percentage: float = 0.0
    duplicate_rows: int = 0
    duplicate_percentage: float = 0.0

    # Column profiles
    column_profiles: dict[str, ColumnProfile] = field(default_factory=dict)

    # Issues
    issues: list[QualityIssue] = field(default_factory=list)

    # Quality score (0-100)
    quality_score: float = 0.0

    # Statistics by data type
    numeric_columns: list[str] = field(default_factory=list)
    string_columns: list[str] = field(default_factory=list)
    datetime_columns: list[str] = field(default_factory=list)
    boolean_columns: list[str] = field(default_factory=list)

    def add_issue(self, issue: QualityIssue) -> None:
        """Add a quality issue to the profile."""
        self.issues.append(issue)

    @property
    def has_issues(self) -> bool:
        """Check if any quality issues exist."""
        return len(self.issues) > 0

    @property
    def high_severity_issues(self) -> list[QualityIssue]:
        """Get all high severity issues."""
        return [issue for issue in self.issues if issue.severity == "high"]

    @property
    def medium_severity_issues(self) -> list[QualityIssue]:
        """Get all medium severity issues."""
        return [issue for issue in self.issues if issue.severity == "medium"]

    @property
    def low_severity_issues(self) -> list[QualityIssue]:
        """Get all low severity issues."""
        return [issue for issue in self.issues if issue.severity == "low"]
