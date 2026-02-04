# Testing to see if we can read the data
import pandas as pd
import yaml

from ingestion.validators import (
    validate_required_columns,
    split_valid_rejects_by_null,
)
from ingestion.loader import load_config, validate_config, ensure_parent_dir
from ingestion.db_loader import load_results_to_postgres
from ingestion.db import get_connection
from ingestion.logging_utils import setup_logger



def run_results_ingestion(config_path: str = "./ingestion/config.yaml") -> None:
    config = load_config(config_path)
    validate_config(config)
    logger = setup_logger(config)

    input_path = config["paths"]["input_path"]
    valid_output_path = config["paths"]["valid_output_path"]
    rejected_output_path = config["paths"]["rejected_output_path"]

    required_columns = config["validation"]["required_columns"]
    key_columns = config["validation"]["key_columns"]

    ensure_parent_dir(input_path)
    ensure_parent_dir(valid_output_path)
    ensure_parent_dir(rejected_output_path)

    # Read CSV
    try:
        results_df = pd.read_csv(input_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input file not found at: {input_path}") from e
    
    # Validate required columns
    validate_required_columns(results_df, required_columns)

    # Split valid vs rejected rows
    valid_df, rejects_df = split_valid_rejects_by_null(results_df, key_columns)

    # Export
    valid_df.to_csv(valid_output_path, index = False)
    rejects_df.to_csv(rejected_output_path, index = False)

    table_name = "stg_results"
    conn = get_connection()
    try:
        inserted = load_results_to_postgres(
            df = valid_df,
            conn = conn,
            table_name = table_name,
            columns = required_columns,
        )
    finally:
        conn.close()

    logger.info("Ingestion complete")
    logger.info(f"Valid rows: {len(valid_df)} -> {valid_output_path}")
    logger.info(f"Rejected rows: {len(rejects_df)} -> {rejected_output_path}")
    logger.info(f"Inserted {inserted} rows into table '{table_name}'")