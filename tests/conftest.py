"""
Pytest configuration and fixtures.
"""

from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def config_path(project_root):
    """Get default configuration file path."""
    return project_root / "config" / "default.yaml"


@pytest.fixture
def sample_data_dir(project_root):
    """Get sample data directory."""
    return project_root / "data" / "samples"
