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

    if "logging" not in config or "log_dir" not in config["logging"]:
        raise ValueError("Missing 'logging.log_dir' in config")
    
    if "datasets" not in config or not isinstance(config["datasets"], dict) or not config["datasets"]:
        raise ValueError("Missing or empty 'datasets' section in config")
    
    required_dataset_keys = [
        "input_path",
        "valid_output_path",
        "rejected_output_path",
        "table_name",
        "required_columns",
        "key_columns",
    ]

    for ds_name, ds in config["datasets"].items():
        if not isinstance(ds, dict):
            raise ValueError(f"datasets.{ds_name} must be a mapping/object")
        
        for key in required_dataset_keys:
            if key not in ds:
                raise ValueError(f"Missing datasets.{ds_name}.{key}")
            
        if not isinstance(ds["required_columns"], list) or not all(isinstance(x, str) for x in ds["required_columns"]):
            raise ValueError(f"datasets.{ds_name}.required_columns must be a list of strings")
        
        if not isinstance(ds["key_columns"], list) or not all(isinstance(x, str) for x in ds["key_columns"]):
            raise ValueError(f"datasets.{ds_name}.key_columns must be a list of strings")
        
        for path_key in ["input_path", "valid_output_path", "rejected_output_path"]:
            if not isinstance(ds[path_key], str) or not ds[path_key].strip():
                raise ValueError(f"datasets.{ds_name}.{path_key} must be a non-empty string")
        
        if not isinstance(ds["table_name"], str) or not ds["table_name"].strip():
            raise ValueError(f"datasets.{ds_name}.table_name must be a non-empty string")
        
def ensure_parent_dir(path_str: str) -> None:
    """
    Create the parent directory for a file path if it doesn't exist.
    """
    Path(path_str).expanduser().resolve().parent.mkdir(parents = True, exist_ok = True)