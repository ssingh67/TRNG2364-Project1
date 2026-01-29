# Testing to see if we can read the data
import pandas as pd
from ingestion.validators import (
    validate_required_columns,
    split_valid_rejects_by_null,
)


def run_results_ingestion():
    """
    Ingests the Formula 1 results dataset by:
    - Reading raw CSV data
    - Performing basic structural validation
    - Separating valid and rejected rows
    - Exporting results to processed and rejects folders
    """

    # Attempt to read the file from the raw results CSV file
    try:
        results_df = pd.read_csv("./data/raw/results.csv")
    except FileNotFoundError:
        print("File Not Found.")
        return

    # Display a preview of the dataset for sanity checking
    print("\nResults DataFrame Head:")
    print(results_df.head())

    # Display DataFrame schema info (columns, types, non-null counts)
    print("\nResults DataFrame Info:")
    results_df.info()

    required_columns = [
        "resultId",
        "raceId",
        "driverId",
        "constructorId",
        "position",
        "points",
    ]

    key_columns = [
        "resultId",
        "raceId",
        "driverId",
        "constructorId",
    ]

    # Validate required columns
    missing_cols = validate_required_columns(results_df, required_columns)
    if missing_cols:
        print(f"\nMissing required columns: {missing_cols}")
        return
    else:
        print("\nNo missing columns\n")

    # Split valid vs rejected rows
    valid_df, rejects_df = split_valid_rejects_by_null(results_df, key_columns)

    # Output basic row counts for verification
    print(f"Valid rows: {len(valid_df)}")
    print(f"Rejected rows: {len(rejects_df)}\n")

    valid_df.to_csv("./data/processed/results_processed.csv", index=False)
    rejects_df.to_csv("./data/rejects/results_rejects.csv", index=False)

    print("Export Complete:")
    print(" - ./data/processed/results_processed.csv")
    print(" - ./data/rejects/results_rejects.csv")
