"""
Data models for PII detection module.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PIIDetection:
    """Represents a detected PII instance."""

    column: str
    row_index: int
    pii_type: str  # e.g., "EMAIL", "PHONE", "SSN", "CREDIT_CARD", "IP_ADDRESS"
    value: str  # The detected PII value
    start_position: int  # Character position in text (for substring matches)
    end_position: int  # End character position
    confidence: float  # 0.0 to 1.0
    detection_method: str  # "rule_based" or "nlp"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate confidence score."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")


@dataclass
class DetectionSummary:
    """Summary of PII detections for a dataset."""

    total_detections: int
    detections_by_type: dict[str, int] = field(default_factory=dict)
    detections_by_column: dict[str, int] = field(default_factory=dict)
    affected_rows: int = 0
    affected_columns: int = 0
    detection_methods: dict[str, int] = field(default_factory=dict)
    confidence_distribution: dict[str, int] = field(default_factory=dict)  # low/medium/high

    @property
    def has_detections(self) -> bool:
        """Check if any PII was detected."""
        return self.total_detections > 0

    def add_detection(self, detection: PIIDetection) -> None:
        """Add a detection to the summary."""
        # Update type counts
        self.detections_by_type[detection.pii_type] = (
            self.detections_by_type.get(detection.pii_type, 0) + 1
        )

        # Update column counts
        self.detections_by_column[detection.column] = (
            self.detections_by_column.get(detection.column, 0) + 1
        )

        # Update method counts
        self.detection_methods[detection.detection_method] = (
            self.detection_methods.get(detection.detection_method, 0) + 1
        )

        # Update confidence distribution
        if detection.confidence >= 0.8:
            conf_level = "high"
        elif detection.confidence >= 0.5:
            conf_level = "medium"
        else:
            conf_level = "low"

        self.confidence_distribution[conf_level] = (
            self.confidence_distribution.get(conf_level, 0) + 1
        )


def create_detection_summary(detections: list[PIIDetection]) -> DetectionSummary:
    """
    Create a summary from a list of detections.

    Args:
        detections: List of PIIDetection objects

    Returns:
        DetectionSummary with aggregated statistics
    """
    summary = DetectionSummary(total_detections=len(detections))

    # Add each detection to summary
    for detection in detections:
        summary.add_detection(detection)

    # Calculate affected rows and columns
    summary.affected_rows = len({d.row_index for d in detections})
    summary.affected_columns = len({d.column for d in detections})

    return summary
