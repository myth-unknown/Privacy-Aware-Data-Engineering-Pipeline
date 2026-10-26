"""
Tests for configuration loader.
"""

import pytest

from src.utils.config_loader import get_config_value, load_config


def test_load_config(config_path):
    """Test loading configuration file."""
    config = load_config(str(config_path))

    assert config is not None
    assert isinstance(config, dict)
    assert 'ingestion' in config
    assert 'detection' in config
    assert 'anonymization' in config


def test_load_config_file_not_found():
    """Test loading non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        load_config('nonexistent.yaml')


def test_get_config_value():
    """Test getting configuration value with dot notation."""
    config = {
        'detection': {
            'rule_based': {
                'email': True,
                'phone': False
            }
        }
    }

    # Test existing values
    assert get_config_value(config, 'detection.rule_based.email') is True
    assert get_config_value(config, 'detection.rule_based.phone') is False

    # Test missing value with default
    assert get_config_value(config, 'detection.missing', default='N/A') == 'N/A'
    assert get_config_value(config, 'totally.missing.key', default=None) is None

    # Test partial path
    rule_based = get_config_value(config, 'detection.rule_based')
    assert isinstance(rule_based, dict)
    assert rule_based['email'] is True


def test_get_config_value_no_default():
    """Test getting missing value without default."""
    config = {'test': 'value'}

    result = get_config_value(config, 'missing.key')
    assert result is None
