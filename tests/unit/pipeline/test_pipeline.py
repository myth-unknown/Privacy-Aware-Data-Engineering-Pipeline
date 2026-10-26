"""
Tests for pipeline orchestration.
"""


from src.pipeline import DataPipeline, PipelineConfig, PipelineResult, PipelineStage


class TestPipelineConfig:
    """Tests for PipelineConfig model."""

    def test_default_config(self):
        """Test default configuration."""
        config = PipelineConfig()

        assert config.file_type == "csv"
        assert config.detection_method == "rule_based"
        assert config.confidence_threshold == 0.5
        assert len(config.enabled_stages) == 4

    def test_custom_config(self):
        """Test custom configuration."""
        config = PipelineConfig(
            file_path="test.csv",
            detection_method="nlp",
            anonymization_strategy="redact",
        )

        assert config.file_path == "test.csv"
        assert config.detection_method == "nlp"
        assert config.anonymization_strategy == "redact"


class TestPipelineResult:
    """Tests for PipelineResult model."""

    def test_pipeline_result_creation(self):
        """Test creating pipeline result."""
        from datetime import datetime

        result = PipelineResult(pipeline_id="test-123", start_time=datetime.now())

        assert result.pipeline_id == "test-123"
        assert result.success is False
        assert len(result.stage_results) == 0

    def test_completed_stages_property(self):
        """Test completed stages property."""
        from datetime import datetime

        from src.pipeline.models import StageResult

        result = PipelineResult(pipeline_id="test", start_time=datetime.now())
        result.add_stage_result(
            StageResult(
                stage=PipelineStage.INGESTION, success=True, duration_seconds=1.0
            )
        )
        result.add_stage_result(
            StageResult(
                stage=PipelineStage.PROFILING, success=True, duration_seconds=0.5
            )
        )

        completed = result.completed_stages
        assert len(completed) == 2
        assert PipelineStage.INGESTION in completed
        assert PipelineStage.PROFILING in completed

    def test_failed_stages_property(self):
        """Test failed stages property."""
        from datetime import datetime

        from src.pipeline.models import StageResult

        result = PipelineResult(pipeline_id="test", start_time=datetime.now())
        result.add_stage_result(
            StageResult(
                stage=PipelineStage.INGESTION, success=False, duration_seconds=1.0
            )
        )

        failed = result.failed_stages
        assert len(failed) == 1
        assert PipelineStage.INGESTION in failed

    def test_has_failures_property(self):
        """Test has failures property."""
        from datetime import datetime

        from src.pipeline.models import StageResult

        result = PipelineResult(pipeline_id="test", start_time=datetime.now())
        assert not result.has_failures

        result.add_stage_result(
            StageResult(
                stage=PipelineStage.INGESTION, success=False, duration_seconds=1.0
            )
        )
        assert result.has_failures

    def test_get_stage_result(self):
        """Test get stage result method."""
        from datetime import datetime

        from src.pipeline.models import StageResult

        result = PipelineResult(pipeline_id="test", start_time=datetime.now())
        stage_result = StageResult(
            stage=PipelineStage.INGESTION, success=True, duration_seconds=1.0
        )
        result.add_stage_result(stage_result)

        retrieved = result.get_stage_result(PipelineStage.INGESTION)
        assert retrieved is not None
        assert retrieved.stage == PipelineStage.INGESTION

        not_found = result.get_stage_result(PipelineStage.STORAGE)
        assert not_found is None


class TestDataPipeline:
    """Tests for DataPipeline class."""

    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        config = PipelineConfig()
        pipeline = DataPipeline(config)

        assert pipeline.config == config
        assert pipeline.result.pipeline_id is not None
        assert pipeline.result.start_time is not None

    def test_pipeline_with_sample_data(self, tmp_path):
        """Test pipeline with actual CSV file."""
        # Create temporary CSV file
        import pandas as pd

        df = pd.DataFrame(
            {
                "name": ["John Doe", "Jane Smith"],
                "email": ["john@example.com", "jane@example.com"],
                "age": [30, 25],
            }
        )
        csv_path = tmp_path / "test.csv"
        df.to_csv(csv_path, index=False)

        # Configure and run pipeline
        config = PipelineConfig(
            file_path=str(csv_path),
            enabled_stages=[
                PipelineStage.INGESTION,
                PipelineStage.PROFILING,
                PipelineStage.DETECTION,
            ],
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        # Verify results
        assert result.success
        assert len(result.completed_stages) == 3
        assert result.original_data is not None
        assert len(result.original_data) == 2

    def test_pipeline_stop_on_error(self, tmp_path):
        """Test pipeline stops on error when configured."""
        # Create config with invalid file
        config = PipelineConfig(
            file_path="nonexistent.csv",
            stop_on_error=True,
            enabled_stages=[PipelineStage.INGESTION, PipelineStage.PROFILING],
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        # Should fail and not continue
        assert not result.success
        assert result.has_failures

    def test_pipeline_profiling_stage(self, tmp_path):
        """Test profiling stage execution."""
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        csv_path = tmp_path / "test.csv"
        df.to_csv(csv_path, index=False)

        config = PipelineConfig(
            file_path=str(csv_path),
            enabled_stages=[PipelineStage.INGESTION, PipelineStage.PROFILING],
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        assert result.success
        assert result.quality_profile is not None
        assert result.quality_profile.num_rows == 3

    def test_pipeline_detection_stage(self, tmp_path):
        """Test detection stage execution."""
        import pandas as pd

        df = pd.DataFrame({"email": ["test@example.com", "user@domain.com"]})
        csv_path = tmp_path / "test.csv"
        df.to_csv(csv_path, index=False)

        config = PipelineConfig(
            file_path=str(csv_path),
            enabled_stages=[PipelineStage.INGESTION, PipelineStage.DETECTION],
            detection_method="rule_based",
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        assert result.success
        assert len(result.detections) >= 2  # Should detect emails


class TestPipelineStages:
    """Tests for individual pipeline stages."""

    def test_ingestion_stage_csv(self, tmp_path):
        """Test CSV ingestion."""
        import pandas as pd

        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        csv_path = tmp_path / "data.csv"
        df.to_csv(csv_path, index=False)

        config = PipelineConfig(
            file_path=str(csv_path), enabled_stages=[PipelineStage.INGESTION]
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        assert result.success
        ingestion_result = result.get_stage_result(PipelineStage.INGESTION)
        assert ingestion_result.success
        assert "2 rows" in ingestion_result.message

    def test_validation_stage_with_duplicates(self, tmp_path):
        """Test validation with duplicate removal."""
        import pandas as pd

        df = pd.DataFrame({"a": [1, 2, 2], "b": [3, 4, 4]})
        csv_path = tmp_path / "data.csv"
        df.to_csv(csv_path, index=False)

        config = PipelineConfig(
            file_path=str(csv_path),
            enabled_stages=[PipelineStage.INGESTION, PipelineStage.VALIDATION],
            clean_data=True,
            remove_duplicates=True,
        )

        pipeline = DataPipeline(config)
        result = pipeline.run()

        assert result.success
        # Should have removed 1 duplicate
        assert len(result.processed_data) == 2
