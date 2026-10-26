"""
Data models for pipeline orchestration.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class PipelineStage(StrEnum):
    """Pipeline execution stages."""

    INGESTION = "ingestion"
    VALIDATION = "validation"
    PROFILING = "profiling"
    DETECTION = "detection"
    ANONYMIZATION = "anonymization"
    STORAGE = "storage"


@dataclass
class StageResult:
    """Result from a single pipeline stage."""

    stage: PipelineStage
    success: bool
    duration_seconds: float
    message: str = ""
    data: Any = None
    error: str | None = None


@dataclass
class PipelineConfig:
    """Configuration for pipeline execution."""

    # Ingestion
    file_path: str = ""
    file_type: str = "csv"  # csv, json
    delimiter: str = ","

    # Validation
    validate_schema: bool = True
    clean_data: bool = False
    remove_duplicates: bool = False

    # Detection
    detection_method: str = "rule_based"  # rule_based, nlp, hybrid
    confidence_threshold: float = 0.5
    columns_to_scan: list[str] | None = None

    # Anonymization
    anonymization_strategy: str = "mask"  # mask, redact, pseudonymize, generalize
    pii_types_to_anonymize: list[str] | None = None

    # Pipeline control
    enabled_stages: list[PipelineStage] = field(
        default_factory=lambda: [
            PipelineStage.INGESTION,
            PipelineStage.PROFILING,
            PipelineStage.DETECTION,
            PipelineStage.ANONYMIZATION,
        ]
    )
    stop_on_error: bool = True
    save_intermediate: bool = False


@dataclass
class PipelineResult:
    """Result from complete pipeline execution."""

    pipeline_id: str
    start_time: datetime
    end_time: datetime | None = None
    success: bool = False
    total_duration_seconds: float = 0.0

    # Stage results
    stage_results: list[StageResult] = field(default_factory=list)

    # Final outputs
    original_data: Any = None
    processed_data: Any = None
    quality_profile: Any = None
    detections: list[Any] = field(default_factory=list)
    anonymization_audit: Any = None

    # Metadata
    config: PipelineConfig | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_stage_result(self, result: StageResult) -> None:
        """Add a stage result."""
        self.stage_results.append(result)

    @property
    def completed_stages(self) -> list[PipelineStage]:
        """Get list of completed stages."""
        return [r.stage for r in self.stage_results if r.success]

    @property
    def failed_stages(self) -> list[PipelineStage]:
        """Get list of failed stages."""
        return [r.stage for r in self.stage_results if not r.success]

    @property
    def has_failures(self) -> bool:
        """Check if any stage failed."""
        return len(self.failed_stages) > 0

    def get_stage_result(self, stage: PipelineStage) -> StageResult | None:
        """Get result for a specific stage."""
        for result in self.stage_results:
            if result.stage == stage:
                return result
        return None
