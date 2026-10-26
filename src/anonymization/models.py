"""
Data models for anonymization module.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AnonymizationConfig:
    """Configuration for anonymization strategies."""

    strategy: str  # "mask", "redact", "pseudonymize", "generalize"
    pii_type: str  # Type of PII to anonymize

    # Strategy-specific parameters
    mask_char: str = "*"
    mask_percentage: float = 0.75  # Percentage to mask (0.0-1.0)
    preserve_format: bool = True  # Preserve original format (e.g., xxx-xx-1234)

    # Pseudonymization
    pseudonym_seed: str | None = None  # Seed for consistent pseudonyms

    # Generalization
    generalization_level: str = "medium"  # "low", "medium", "high"

    # Metadata
    apply_to_columns: list[str] | None = None  # Specific columns (None = all)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformationRecord:
    """Record of a single transformation."""

    column: str
    row_index: int
    pii_type: str
    original_value: str
    transformed_value: str
    strategy: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformationAudit:
    """Audit trail of all transformations."""

    total_transformations: int = 0
    transformations_by_type: dict[str, int] = field(default_factory=dict)
    transformations_by_strategy: dict[str, int] = field(default_factory=dict)
    transformations_by_column: dict[str, int] = field(default_factory=dict)

    # Detailed records (optional, can be large)
    records: list[TransformationRecord] = field(default_factory=list)

    # Summary
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def duration_seconds(self) -> float | None:
        """Calculate transformation duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def add_record(self, record: TransformationRecord) -> None:
        """Add a transformation record to the audit."""
        self.records.append(record)
        self.total_transformations += 1

        # Update counts
        self.transformations_by_type[record.pii_type] = (
            self.transformations_by_type.get(record.pii_type, 0) + 1
        )
        self.transformations_by_strategy[record.strategy] = (
            self.transformations_by_strategy.get(record.strategy, 0) + 1
        )
        self.transformations_by_column[record.column] = (
            self.transformations_by_column.get(record.column, 0) + 1
        )

    @property
    def has_transformations(self) -> bool:
        """Check if any transformations were performed."""
        return self.total_transformations > 0


@dataclass
class AnonymizationResult:
    """Result of anonymization process."""

    success: bool
    data: Any  # Anonymized DataFrame
    audit: TransformationAudit
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        """Check if any errors occurred."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if any warnings occurred."""
        return len(self.warnings) > 0
