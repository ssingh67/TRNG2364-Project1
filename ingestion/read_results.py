# Testing to see if we can read the data
import pandas as pd
import numpy as np

from ingestion.validators import (
    validate_required_columns,
    split_valid_rejects_by_null,
)
from ingestion.loader import load_config, validate_config, ensure_parent_dir
from ingestion.logging_utils import setup_logger

from backend.db import get_conn
from backend.load_results_postgres import load_results_to_postgres
from backend.settings import STG_RESULTS_FULL_TABLE


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

    results_df = results_df.rename(columns = {
        "resultId": "result_id",
        "raceId": "race_id",
        "driverId": "driver_id",
        "constructorId": "constructor_id",
    })

    results_df = results_df.replace(r'\\N', np.nan, regex = True)
    
    # Ensuring numeric columns are numeric (bad values -> NaN -> NULL after loader fix)
    results_df["position"] = pd.to_numeric(results_df["position"], errors = "coerce")
    results_df["points"] = pd.to_numeric(results_df["points"], errors="coerce")

    db_columns = [
    "result_id",
    "race_id",
    "driver_id",
    "constructor_id",
    "position",
    "points",
    ]

    key_columns_db = [
        "result_id",
        "race_id",
        "driver_id",
        "constructor_id",
    ]

    # Split valid vs rejected rows
    valid_df, rejects_df = split_valid_rejects_by_null(results_df, key_columns_db)

    # Export
    valid_df.to_csv(valid_output_path, index = False)
    rejects_df.to_csv(rejected_output_path, index = False)

    logger.info("Ingestion complete")
    logger.info(f"Valid rows: {len(valid_df)} -> {valid_output_path}")
    logger.info(f"Rejected rows: {len(rejects_df)} -> {rejected_output_path}")

    logger.info(
        f"Loading {len(valid_df)} valid rows into DB table: {STG_RESULTS_FULL_TABLE}"
    )

    conn = get_conn()
    try:
        inserted = load_results_to_postgres(
            df = valid_df,
            conn = conn,
            table_name = STG_RESULTS_FULL_TABLE,
            columns = db_columns,
            page_size = 1000,
        )
        logger.info(f"DB load complete. Inserted rows: {inserted}")
    finally:
        conn.close()