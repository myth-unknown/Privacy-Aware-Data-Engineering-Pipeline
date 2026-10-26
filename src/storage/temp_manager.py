"""
Temporary file management for pipeline processing.
"""

import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class TempFileManager:
    """Manages temporary files during pipeline execution."""

    def __init__(self, base_dir: str = None):
        """
        Initialize temp file manager.

        Args:
            base_dir: Base directory for temp files (uses system temp if None)
        """
        self.base_dir = Path(base_dir) if base_dir else None
        self.created_files = []
        logger.info("TempFileManager initialized")

    def create_temp_file(self, suffix: str = ".csv", prefix: str = "pipeline_") -> str:
        """
        Create a temporary file.

        Args:
            suffix: File extension
            prefix: Filename prefix

        Returns:
            Path to temporary file
        """
        if self.base_dir:
            self.base_dir.mkdir(parents=True, exist_ok=True)
            temp_file = tempfile.NamedTemporaryFile(
                suffix=suffix, prefix=prefix, dir=self.base_dir, delete=False
            )
        else:
            temp_file = tempfile.NamedTemporaryFile(
                suffix=suffix, prefix=prefix, delete=False
            )

        temp_path = temp_file.name
        temp_file.close()
        self.created_files.append(temp_path)

        logger.debug(f"Created temp file: {temp_path}")
        return temp_path

    def cleanup(self):
        """Remove all created temporary files."""
        for file_path in self.created_files:
            try:
                Path(file_path).unlink(missing_ok=True)
                logger.debug(f"Removed temp file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temp file {file_path}: {e}")

        self.created_files.clear()
        logger.info("Cleanup complete")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
