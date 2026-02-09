# Testing to see if we can read the data
import pandas as pd
import numpy as np

from ingestion.validators import validate_required_columns, split_valid_rejects_by_required_not_null
from ingestion.loader import load_config, validate_config, ensure_parent_dir
from ingestion.logging_utils import setup_logger
from ingestion.cleaners import deduplicate

from backend.db import get_conn
from backend.load_csvs_postgres import load_dataframe_to_postgres


def _apply_dataset_transforms(dataset_name: str, df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace(r"\\+N", np.nan, regex = True)

    if dataset_name == "results":
        df = df.rename(
            columns = {
                "resultId": "result_id",
                "raceId": "race_id",
                "driverId": "driver_id",
                "constructorId": "constructor_id",
            }
        )

        if "position" in df.columns:
            df["position"] = pd.to_numeric(df["position"], errors = "coerce")
        
        if "points" in df.columns:
            df["points"] = pd.to_numeric(df["points"], errors = "coerce")
        
    return df

def run_all_ingestion(config_path: str = "./ingestion/config.yaml", load_results_to_db: bool = True) -> None:
    config = load_config(config_path)
    validate_config(config)
    logger = setup_logger(config)

    for dataset_name, ds in config["datasets"].items():
        input_path = ds["input_path"]
        valid_output_path = ds["valid_output_path"]
        rejected_output_path = ds["rejected_output_path"]
        table_name = ds["table_name"]

        required_columns = ds["required_columns"]
        key_columns = ds["key_columns"]

        ensure_parent_dir(valid_output_path)
        ensure_parent_dir(rejected_output_path)

        logger.info(f"--- Starting ingestion: {dataset_name} ---")
        logger.info(f"Reading: {input_path}")

        # Read CSV
        try:
            df = pd.read_csv(input_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input file not found at: {input_path}") from e
        
        # Validate required columns
        validate_required_columns(df, required_columns)

        # Apply the transformations
        df = _apply_dataset_transforms(dataset_name, df)

        # Key columns must match df at this point.
        # For results, config uses camelCase but df is now snake_case.
        if dataset_name == "results":
            key_columns_effective = ["result_id", "race_id", "driver_id", "constructor_id"]
        else:
            key_columns_effective = key_columns
        
        df = deduplicate(df, key_columns_effective)

        if dataset_name == "results":
            required_not_null = key_columns_effective + ["points"]
        elif dataset_name == "races":
            required_not_null = ["raceId"]
        elif dataset_name == "drivers":
            required_not_null = ["driverId"]
        elif dataset_name == "constructor":
            required_not_null = ["constructorId"]
        else:
            required_not_null = key_columns_effective
        
        valid_df, rejects_df = split_valid_rejects_by_required_not_null(df, required_not_null)

        valid_df.to_csv(valid_output_path, index = False)
        rejects_df.to_csv(rejected_output_path, index = False)

        logger.info(f"{dataset_name}: Valid rows: {len(valid_df)} -> {valid_output_path}")
        logger.info(f"{dataset_name}: Rejected rows: {len(rejects_df)} -> {rejected_output_path}")

        # DB load: keep it to results only for now
        if load_results_to_db and dataset_name == "results":
            db_columns = [
                "result_id",
                "race_id",
                "driver_id",
                "constructor_id",
                "position",
                "points",
            ]

            logger.info(f"Loading {len(valid_df)} valid rows into DB table: {table_name}")

            conn = get_conn()
            try:
                inserted = load_dataframe_to_postgres(
                    df = valid_df,
                    conn = conn,
                    table_name = table_name,
                    columns = db_columns,
                    page_size = 1000,
                    truncate_first = True
                )
                
                logger.info(f"DB load complete. Inserted rows: {inserted}")
            finally:
                conn.close()
        
        logger.info(f"--- Finished ingestion: {dataset_name} ---")
    logger.info("All dataset ingestions complete.")