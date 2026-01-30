from pathlib import Path
import yaml

def load_config(config_path: str = "ingestion/config.yaml") -> dict:
    """
    Load ingestion configuration from a YAML file
    """
    with open(config_path, "r", encoding = "utf-8") as f:
        return yaml.safe_load(f)
    
def validate_config(config: dict) -> None:
    """
    Validate required structure of ingestion config.
    Raises ValueError if config is invalid.
    """
    required_paths = [
        "input_path",
        "valid_output_path",
        "rejected_output_path",
    ]

    required_validation = [
        "required_columns",
        "key_columns",
    ]

    if "paths" not in config:
        raise ValueError("Missing 'paths' section in config")
    
    if "validation" not in config:
        raise ValueError("Missing 'validation' section in config")
    
    for key in required_paths:
        if key not in config["paths"]:
            raise ValueError(f"Missing config.paths.{key}")
    
    for key in required_validation:
        if key not in config["validation"]:
            raise ValueError(f"Missing config.validation.{key}")
        
def ensure_parent_dir(path_str: str) -> None:
    """
    Create the parent directory for a file path if it doesn't exist.
    """
    Path(path_str).expanduser().resolve().parent.mkdir(parents = True, exist_ok = True)