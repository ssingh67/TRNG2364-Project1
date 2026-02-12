# Testing to see if we can read the data
import pandas as pd
import numpy as np

from ingestion.validators import validate_required_columns, split_valid_rejects_by_required_not_null
from ingestion.loader import load_config, validate_config, ensure_parent_dir
from ingestion.logging_utils import setup_logger
from ingestion.cleaners import deduplicate

from backend.db import get_conn
from backend.load_csvs_postgres import load_dataframe_to_postgres


def _apply_dataset_transforms(dataset_name: str, ds: dict, df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace(r"\\N", np.nan, regex=True)

    rename_map = ds.get("rename_map", {})
    if rename_map:
        df = df.rename(columns=rename_map)

    keep_columns = ds.get("keep_columns")
    if keep_columns:
        df = df[[c for c in keep_columns if c in df.columns]]

    if dataset_name == "results":
        if "position" in df.columns:
            df["position"] = pd.to_numeric(df["position"], errors="coerce")
        if "points" in df.columns:
            df["points"] = pd.to_numeric(df["points"], errors="coerce")

    return df

def run_all_ingestion(config_path: str = "./ingestion/config.yaml", load_datasets_to_db: bool = True) -> None:
    config = load_config(config_path)
    validate_config(config)
    logger = setup_logger(config)

    for dataset_name, ds in config["datasets"].items():
        input_path = ds["input_path"]
        valid_output_path = ds["valid_output_path"]
        rejected_output_path = ds["rejected_output_path"]
        table_name = ds["table_name"]

        required_columns = ds["required_columns"]
        dedupe_keys = ds["dedupe_keys"]
        db_columns = ds["db_columns"]

        ensure_parent_dir(valid_output_path)
        ensure_parent_dir(rejected_output_path)

        logger.info(f"--- Starting ingestion: {dataset_name} ---")
        logger.info(f"Reading: {input_path}")

        # Read CSV
        try:
            df = pd.read_csv(input_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input file not found at: {input_path}") from e
        
        logger.info(f"{dataset_name}: Raw columns: {list(df.columns)}")
        
        # Validate required columns
        validate_required_columns(df, required_columns)

        # Apply the transformations
        df = _apply_dataset_transforms(dataset_name, ds, df)

        logger.info(f"{dataset_name}: Transformed columns: {list(df.columns)}")

        missing_keys = [c for c in dedupe_keys if c not in df.columns]
        if missing_keys:
            raise ValueError(
                f"{dataset_name}: dedupe_keys not found after transforms: {missing_keys}. "
                f"Available columns: {list(df.columns)}"
            )

        # Deduplicate (after transforms, so keys match final column names)
        df = deduplicate(df, dedupe_keys)

        # Required not null: use the dedupe keys for every dataset
        required_not_null = dedupe_keys.copy()
        if dataset_name == "results":
            required_not_null += ["points"]
        
        valid_df, rejects_df = split_valid_rejects_by_required_not_null(df, required_not_null)

        valid_df.to_csv(valid_output_path, index = False)
        rejects_df.to_csv(rejected_output_path, index = False)

        logger.info(f"{dataset_name}: Valid rows: {len(valid_df)} -> {valid_output_path}")
        logger.info(f"{dataset_name}: Rejected rows: {len(rejects_df)} -> {rejected_output_path}")

        # DB load: All datasets now
        if load_datasets_to_db:
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