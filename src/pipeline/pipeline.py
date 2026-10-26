"""
End-to-end data processing pipeline orchestrator.
"""

import logging
import time
import uuid
from datetime import datetime

from src.anonymization import anonymize_dataframe
from src.detection import create_detector
from src.ingestion import load_csv, load_json, validate_dataframe
from src.pipeline.models import (
    PipelineConfig,
    PipelineResult,
    PipelineStage,
    StageResult,
)
from src.validation import profile_dataframe
from src.validation.cleaner import remove_duplicates

logger = logging.getLogger(__name__)


class DataPipeline:
    """
    End-to-end data processing pipeline.

    Orchestrates the complete flow: ingestion → validation → profiling →
    detection → anonymization → storage.
    """

    def __init__(self, config: PipelineConfig):
        """
        Initialize pipeline with configuration.

        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.result = PipelineResult(
            pipeline_id=str(uuid.uuid4()),
            start_time=datetime.now(),
            config=config,
        )
        logger.info(f"Pipeline initialized: {self.result.pipeline_id}")

    def run(self) -> PipelineResult:
        """
        Execute the complete pipeline.

        Returns:
            PipelineResult with outputs and stage results
        """
        logger.info(f"Starting pipeline execution: {self.result.pipeline_id}")
        pipeline_start = time.time()

        try:
            # Execute each enabled stage
            for stage in self.config.enabled_stages:
                stage_result = self._execute_stage(stage)
                self.result.add_stage_result(stage_result)

                if not stage_result.success:
                    logger.error(f"Stage {stage} failed: {stage_result.error}")
                    if self.config.stop_on_error:
                        logger.info("Stopping pipeline due to stage failure")
                        break

            # Mark pipeline success if no failures
            self.result.success = not self.result.has_failures

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}", exc_info=True)
            self.result.success = False
            # Add error stage result
            self.result.add_stage_result(
                StageResult(
                    stage=PipelineStage.INGESTION,  # Generic
                    success=False,
                    duration_seconds=0.0,
                    error=str(e),
                )
            )

        finally:
            # Finalize result
            self.result.end_time = datetime.now()
            self.result.total_duration_seconds = time.time() - pipeline_start

            logger.info(
                f"Pipeline completed: success={self.result.success}, "
                f"duration={self.result.total_duration_seconds:.2f}s"
            )

        return self.result

    def _execute_stage(self, stage: PipelineStage) -> StageResult:
        """Execute a single pipeline stage."""
        logger.info(f"Executing stage: {stage}")
        start_time = time.time()

        try:
            if stage == PipelineStage.INGESTION:
                return self._run_ingestion(start_time)
            elif stage == PipelineStage.VALIDATION:
                return self._run_validation(start_time)
            elif stage == PipelineStage.PROFILING:
                return self._run_profiling(start_time)
            elif stage == PipelineStage.DETECTION:
                return self._run_detection(start_time)
            elif stage == PipelineStage.ANONYMIZATION:
                return self._run_anonymization(start_time)
            elif stage == PipelineStage.STORAGE:
                return self._run_storage(start_time)
            else:
                raise ValueError(f"Unknown stage: {stage}")

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Stage {stage} failed: {e}", exc_info=True)
            return StageResult(
                stage=stage,
                success=False,
                duration_seconds=duration,
                error=str(e),
            )

    def _run_ingestion(self, start_time: float) -> StageResult:
        """Run ingestion stage."""
        # Load data
        if self.config.file_type == "csv":
            df = load_csv(self.config.file_path, delimiter=self.config.delimiter)
        elif self.config.file_type == "json":
            df = load_json(self.config.file_path)
        else:
            raise ValueError(f"Unsupported file type: {self.config.file_type}")

        # Validate
        validation_result = validate_dataframe(df)
        if not validation_result.success:
            error_msg = f"Validation failed: {len(validation_result.issues)} issues"
            return StageResult(
                stage=PipelineStage.INGESTION,
                success=False,
                duration_seconds=time.time() - start_time,
                error=error_msg,
            )

        # Store data
        self.result.original_data = df
        self.result.processed_data = df.copy()

        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.INGESTION,
            success=True,
            duration_seconds=duration,
            message=f"Loaded {len(df)} rows, {len(df.columns)} columns",
            data=df,
        )

    def _run_validation(self, start_time: float) -> StageResult:
        """Run validation/cleaning stage."""
        df = self.result.processed_data

        if self.config.clean_data:
            # Remove duplicates if configured
            if self.config.remove_duplicates:
                original_count = len(df)
                df = remove_duplicates(df)
                removed = original_count - len(df)
                logger.info(f"Removed {removed} duplicate rows")

        self.result.processed_data = df

        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.VALIDATION,
            success=True,
            duration_seconds=duration,
            message=f"Validation complete: {len(df)} rows",
            data=df,
        )

    def _run_profiling(self, start_time: float) -> StageResult:
        """Run profiling stage."""
        df = self.result.processed_data

        # Profile data quality
        profile = profile_dataframe(df)
        self.result.quality_profile = profile

        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.PROFILING,
            success=True,
            duration_seconds=duration,
            message=f"Quality score: {profile.quality_score:.1f}/100",
            data=profile,
        )

    def _run_detection(self, start_time: float) -> StageResult:
        """Run PII detection stage."""
        df = self.result.processed_data

        # Create detector
        detector = create_detector(self.config.detection_method)

        # Run detection
        detections = detector.detect(df)

        # Filter by confidence and columns
        if self.config.columns_to_scan:
            detections = [
                d for d in detections if d.column in self.config.columns_to_scan
            ]

        detections = [
            d
            for d in detections
            if d.confidence >= self.config.confidence_threshold
        ]

        self.result.detections = detections

        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.DETECTION,
            success=True,
            duration_seconds=duration,
            message=f"Detected {len(detections)} PII instances",
            data=detections,
        )

    def _run_anonymization(self, start_time: float) -> StageResult:
        """Run anonymization stage."""
        df = self.result.processed_data
        detections = self.result.detections

        if not detections:
            logger.info("No detections to anonymize")
            return StageResult(
                stage=PipelineStage.ANONYMIZATION,
                success=True,
                duration_seconds=time.time() - start_time,
                message="No PII to anonymize",
            )

        # Determine PII types to anonymize
        pii_types = self.config.pii_types_to_anonymize
        if pii_types is None:
            pii_types = "ALL"
        else:
            # Filter detections
            detections = [d for d in detections if d.pii_type in pii_types]

        # Anonymize
        result = anonymize_dataframe(
            df,
            detections,
            strategy=self.config.anonymization_strategy,
            pii_type=pii_types,
        )

        self.result.processed_data = result.anonymized_data
        self.result.anonymization_audit = result.audit

        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.ANONYMIZATION,
            success=True,
            duration_seconds=duration,
            message=f"Anonymized {result.audit.total_transformations} values",
            data=result,
        )

    def _run_storage(self, start_time: float) -> StageResult:
        """Run storage stage (placeholder for M10)."""
        # Placeholder - will be implemented in M10
        duration = time.time() - start_time
        return StageResult(
            stage=PipelineStage.STORAGE,
            success=True,
            duration_seconds=duration,
            message="Storage not yet implemented (M10)",
        )


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    """
    Convenience function to run pipeline.

    Args:
        config: Pipeline configuration

    Returns:
        PipelineResult
    """
    pipeline = DataPipeline(config)
    return pipeline.run()
