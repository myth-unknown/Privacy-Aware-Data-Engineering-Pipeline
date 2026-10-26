"""
Data models for ingestion module.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IssueSeverity(Enum):
    """Severity levels for validation issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationIssue:
    """Represents a validation issue found during ingestion."""

    severity: IssueSeverity
    message: str
    column: str | None = None
    row: int | None = None
    details: dict[str, Any] | None = None


@dataclass
class IngestionResult:
    """Result of data ingestion process."""

    success: bool
    data: Any | None = None
    file_name: str | None = None
    file_size_bytes: int | None = None
    encoding: str | None = None
    num_rows: int | None = None
    num_columns: int | None = None
    column_names: list[str] | None = None
    issues: list[ValidationIssue] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_errors(self) -> bool:
        """Check if any ERROR level issues exist."""
        return any(issue.severity == IssueSeverity.ERROR for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Check if any WARNING level issues exist."""
        return any(issue.severity == IssueSeverity.WARNING for issue in self.issues)

    def add_issue(
        self,
        severity: IssueSeverity,
        message: str,
        column: str | None = None,
        row: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Add a validation issue to the result."""
        self.issues.append(
            ValidationIssue(
                severity=severity,
                message=message,
                column=column,
                row=row,
                details=details,
            )
        )
