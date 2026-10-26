"""
Data models for method comparison.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MethodMetrics:
    """Performance metrics for a detection method."""

    method_name: str  # "rule_based", "nlp", "hybrid"

    # Detection counts
    total_detections: int = 0
    detections_by_type: dict[str, int] = field(default_factory=dict)

    # Performance metrics
    execution_time_seconds: float = 0.0
    throughput_rows_per_second: float = 0.0

    # Coverage
    columns_scanned: int = 0
    rows_scanned: int = 0
    cells_with_pii: int = 0
    pii_percentage: float = 0.0

    # Confidence distribution
    high_confidence_count: int = 0  # >= 0.8
    medium_confidence_count: int = 0  # 0.5-0.8
    low_confidence_count: int = 0  # < 0.5
    avg_confidence: float = 0.0


@dataclass
class ComparisonResult:
    """Results of comparing multiple detection methods."""

    timestamp: datetime = field(default_factory=datetime.now)

    # Dataset metadata
    dataset_name: str = ""
    total_rows: int = 0
    total_columns: int = 0

    # Method metrics
    method_metrics: dict[str, MethodMetrics] = field(default_factory=dict)

    # Comparison insights
    agreement_count: int = 0  # PII found by all methods
    disagreement_count: int = 0  # PII found by only some methods
    unique_to_rule_based: int = 0
    unique_to_nlp: int = 0
    unique_to_hybrid: int = 0

    # Recommendations
    recommended_method: str = ""
    recommendation_reason: str = ""

    def add_method_metrics(self, metrics: MethodMetrics) -> None:
        """Add metrics for a detection method."""
        self.method_metrics[metrics.method_name] = metrics

    @property
    def methods_compared(self) -> list[str]:
        """Get list of compared methods."""
        return list(self.method_metrics.keys())

    @property
    def fastest_method(self) -> str:
        """Get name of fastest method."""
        if not self.method_metrics:
            return ""
        return min(
            self.method_metrics.items(),
            key=lambda x: x[1].execution_time_seconds,
        )[0]

    @property
    def most_detections_method(self) -> str:
        """Get name of method with most detections."""
        if not self.method_metrics:
            return ""
        return max(
            self.method_metrics.items(),
            key=lambda x: x[1].total_detections,
        )[0]

    @property
    def highest_confidence_method(self) -> str:
        """Get name of method with highest average confidence."""
        if not self.method_metrics:
            return ""
        return max(
            self.method_metrics.items(),
            key=lambda x: x[1].avg_confidence,
        )[0]
