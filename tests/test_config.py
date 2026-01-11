import pytest
import os
from src.config import load_config

def test_config_loading():
    config = load_config("config/config.yaml")
    assert "project" in config
    assert config["project"]["name"] == "crop_yield_prediction"
    assert "paths" in config
    assert "model" in config

def test_config_fail_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yaml")
