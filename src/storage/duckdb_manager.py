"""
DuckDB database management for storing pipeline results.
"""

import logging
from datetime import datetime
from pathlib import Path

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)


class DuckDBManager:
    """Manages DuckDB database operations."""

    def __init__(self, db_path: str = "data/pipeline.duckdb"):
        """
        Initialize DuckDB manager.

        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        logger.info(f"DuckDB manager initialized: {self.db_path}")

    def connect(self):
        """Connect to database."""
        if self.conn is None:
            self.conn = duckdb.connect(str(self.db_path))
            self._initialize_schema()
            logger.info("Connected to DuckDB")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Closed DuckDB connection")

    def _initialize_schema(self):
        """Initialize database schema."""
        # Datasets table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS datasets (
                dataset_id VARCHAR PRIMARY KEY,
                name VARCHAR,
                uploaded_at TIMESTAMP,
                num_rows INTEGER,
                num_columns INTEGER,
                file_size_bytes INTEGER,
                metadata JSON
            )
        """)

        # Pipeline runs table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id VARCHAR PRIMARY KEY,
                dataset_id VARCHAR,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                success BOOLEAN,
                duration_seconds DOUBLE,
                config JSON,
                FOREIGN KEY (dataset_id) REFERENCES datasets(dataset_id)
            )
        """)

        # Detections table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                detection_id VARCHAR PRIMARY KEY,
                run_id VARCHAR,
                row_index INTEGER,
                column_name VARCHAR,
                pii_type VARCHAR,
                confidence DOUBLE,
                detection_method VARCHAR,
                detected_at TIMESTAMP,
                FOREIGN KEY (run_id) REFERENCES pipeline_runs(run_id)
            )
        """)

        logger.info("Database schema initialized")

    def save_dataset(
        self, dataset_id: str, name: str, df: pd.DataFrame, metadata: dict = None
    ) -> None:
        """Save dataset metadata."""
        self.connect()

        self.conn.execute(
            """
            INSERT OR REPLACE INTO datasets
            (dataset_id, name, uploaded_at, num_rows, num_columns, file_size_bytes, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [
                dataset_id,
                name,
                datetime.now(),
                len(df),
                len(df.columns),
                df.memory_usage(deep=True).sum(),
                metadata or {},
            ],
        )

        logger.info(f"Saved dataset: {dataset_id}")

    def save_pipeline_run(self, run_result) -> None:
        """Save pipeline run result."""
        self.connect()

        self.conn.execute(
            """
            INSERT OR REPLACE INTO pipeline_runs
            (run_id, dataset_id, started_at, completed_at, success, duration_seconds, config)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            [
                run_result.pipeline_id,
                run_result.metadata.get("dataset_id", "unknown"),
                run_result.start_time,
                run_result.end_time,
                run_result.success,
                run_result.total_duration_seconds,
                {},  # config dict
            ],
        )

        logger.info(f"Saved pipeline run: {run_result.pipeline_id}")

    def save_detections(self, run_id: str, detections: list) -> None:
        """Save PII detections."""
        self.connect()

        for detection in detections:
            detection_id = f"{run_id}_{detection.row_index}_{detection.column}"
            self.conn.execute(
                """
                INSERT OR REPLACE INTO detections
                (detection_id, run_id, row_index, column_name, pii_type, confidence, detection_method, detected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    detection_id,
                    run_id,
                    detection.row_index,
                    detection.column,
                    detection.pii_type,
                    detection.confidence,
                    detection.detection_method,
                    datetime.now(),
                ],
            )

        logger.info(f"Saved {len(detections)} detections for run {run_id}")

    def get_recent_runs(self, limit: int = 10) -> pd.DataFrame:
        """Get recent pipeline runs."""
        self.connect()
        return self.conn.execute(
            """
            SELECT * FROM pipeline_runs
            ORDER BY started_at DESC
            LIMIT ?
        """,
            [limit],
        ).df()

    def get_datasets(self) -> pd.DataFrame:
        """Get all datasets."""
        self.connect()
        return self.conn.execute("SELECT * FROM datasets ORDER BY uploaded_at DESC").df()

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
