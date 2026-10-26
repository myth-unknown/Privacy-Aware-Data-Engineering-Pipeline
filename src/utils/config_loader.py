"""
Configuration loader utility.

Loads configuration from YAML files and environment variables.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


def load_config(config_path: str = "config/default.yaml") -> dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file.

    Returns:
        Configuration dictionary.

    Raises:
        FileNotFoundError: If configuration file not found.
        yaml.YAMLError: If YAML parsing fails.
    """
    # Load environment variables from .env if present
    load_dotenv()

    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Override with environment variables if present
    config = _apply_env_overrides(config)

    return config


def get_config_value(config: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Get configuration value using dot notation.

    Args:
        config: Configuration dictionary.
        key: Dot-separated key path (e.g., 'detection.rule_based.email').
        default: Default value if key not found.

    Returns:
        Configuration value or default.

    Examples:
        >>> config = {'detection': {'rule_based': {'email': True}}}
        >>> get_config_value(config, 'detection.rule_based.email')
        True
        >>> get_config_value(config, 'detection.missing', default=False)
        False
    """
    keys = key.split('.')
    value = config

    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return default
        else:
            return default

    return value


def _apply_env_overrides(config: dict[str, Any]) -> dict[str, Any]:
    """
    Apply environment variable overrides to configuration.

    Args:
        config: Configuration dictionary.

    Returns:
        Configuration with environment overrides applied.
    """
    # Define mappings from environment variables to config keys
    env_mappings = {
        'PIPELINE_MAX_FILE_SIZE_MB': 'ingestion.max_file_size_mb',
        'PIPELINE_MAX_ROWS': 'ingestion.max_rows',
        'DUCKDB_PATH': 'storage.database_path',
        'SPACY_MODEL': 'detection.nlp_assisted.model',
        'PSEUDONYM_KEY': 'anonymization.pseudo_key',
        'LOG_LEVEL': 'logging.level',
        'LOG_FILE': 'logging.file',
    }

    for env_var, config_key in env_mappings.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Set nested config value
            keys = config_key.split('.')
            current = config
            for _i, key in enumerate(keys[:-1]):
                if key not in current:
                    current[key] = {}
                current = current[key]

            # Convert value to appropriate type
            final_key = keys[-1]
            if env_var in ['PIPELINE_MAX_FILE_SIZE_MB', 'PIPELINE_MAX_ROWS']:
                current[final_key] = int(env_value)
            else:
                current[final_key] = env_value

    return config
