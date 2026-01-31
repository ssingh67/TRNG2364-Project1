from ingestion.loader import load_config

def test_load_config_returns_dict():
    config = load_config("ingestion/config.yaml")
    assert isinstance(config, dict)

def test_required_top_level_keys_exist():
    config = load_config("ingestion/config.yaml")

    assert "paths" in config
    assert "logging" in config
    assert "validation" in config