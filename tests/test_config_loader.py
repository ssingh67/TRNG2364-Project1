import pytest
from ingestion.loader import load_config, validate_config

def test_load_config_returns_dict():
    config = load_config("ingestion/config.yaml")
    assert isinstance(config, dict)

def test_required_top_level_keys_exist():
    config = load_config("ingestion/config.yaml")

    assert "logging" in config
    assert "datasets" in config
    assert isinstance(config["datasets"], dict)
    assert len(config["datasets"]) > 0

def test_validate_config_accepts_real_config():
    config = load_config("ingestion/config.yaml")
    validate_config(config)

    assert True

def test_validate_config_raises_when_logging_missing():
    bad_config = {
        "datasets": {
            "results": {
                "input_path": "./data/raw/results.csv",
                "valid_output_path": "./data/processed/results_processed.csv",
                "rejected_output_path": "./data/rejects/results_rejects.csv",
                "table_name": "staging.stg_results",
                "required_columns": ["resultId"],
                "key_columns": ["resultId"],                
            }
        }
    }

    with pytest.raises(ValueError):
        validate_config(bad_config)

def test_validate_config_raises_when_datasets_missing():
    bad_config = {"logging": {"log_dir": "data/logs"}}

    with pytest.raises(ValueError):
        validate_config(bad_config)

def test_validate_config_raises_when_dataset_missing_required_key():
    bad_config = {
        "logging": {"log_dir": "data/logs"},
        "datasets": {
            "results": {
                "valid_output_path": "./data/processed/results_processed.csv",
                "rejected_output_path": "./data/rejects/results_rejects.csv",
                "table_name": "staging.stg_results",
                "required_columns": ["resultId"],
                "key_columns": ["resultId"],
            }
        },
    }

    with pytest.raises(ValueError):
        validate_config(bad_config)

def test_validate_config_raises_when_required_columns_not_list_of_strings():
    bad_config = {
        "logging": {"log_dir": "data/logs"},
        "datasets": {
            "results": {
                "input_path": "./data/raw/results.csv",
                "valid_output_path": "./data/processed/results_processed.csv",
                "rejected_output_path": "./data/rejects/results_rejects.csv",
                "table_name": "staging.stg_results",
                "required_columns": [123],  # invalid
                "key_columns": ["resultId"],
            }
        },
    }

    with pytest.raises(ValueError):
        validate_config(bad_config)

def test_validate_config_raises_when_key_columns_not_list_of_strings():
    bad_config = {
        "logging": {"log_dir": "data/logs"},
        "datasets": {
            "results": {
                "input_path": "./data/raw/results.csv",
                "valid_output_path": "./data/processed/results_processed.csv",
                "rejected_output_path": "./data/rejects/results_rejects.csv",
                "table_name": "staging.stg_results",
                "required_columns": ["resultId"],
                "key_columns": [["resultId"]],  # invalid (nested list)
            }
        },
    }

    with pytest.raises(ValueError):
        validate_config(bad_config)