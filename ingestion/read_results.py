# Testing to see if we can read the data
import pandas as pd


def run_results_ingestion():
    """
    Ingests the Formula 1 results dataset by:
    - Reading raw CSV data
    - Performing basic structural validation
    - Separating valid and rejected rows
    - Exporting results to processed and rejects folders
    """

    # Attempt to read the file from the raw results CSV file
    # If file does not exist, stop the ingestion process early
    try:
        results_df = pd.read_csv("./data/raw/results.csv")

    except FileNotFoundError:
        print("File Not Found.")
        return

    # Display a preview of the dataset for sanity checking
    print("\nResults DataFrame Head:")
    print(results_df.head())

    # Display DataFrame schema info (columns, types, non-null counts)
    print(f"\nResults DataFrame Info:")
    results_df.info()

    # -------------------------------------------------------------------------
    # VALIDATION LOGIC (You can delete this when you are done moving the code below into validators.py)
    # NOTE:
    # - This validation logic will be refactored into ingestion/validators.py
    # - read_results.py should only orchestrate ingestion steps
    # - validators.py should contain reusable validation functions
    # -------------------------------------------------------------------------

    # Define the minimum set of columns required for a valid race result
    # These columns ensure teh row is structurally usable
    required_columns = [
        "resultId",
        "raceId",
        "driverId",
        "constructorId",
        "position",
        "points",
    ]

    # Check for any required columns missing from the dataset
    missing_cols = [col for col in required_columns if col not in results_df.columns]

    # If there are missing columns then stop the ingestion, otherwise print no missing columns
    if missing_cols:
        print(f"\nMissing required columns: {missing_cols}")
        return
    else:
        print("\nNo missing columns\n")

    # Columns that must not contain null values for a row to be considered valid
    key_cols = ["resultId", "raceId", "driverId", "constructorId"]

    # Create a boolean mask identifying rows with missing values in key columns
    reject_mask = results_df[key_cols].isna().any(axis = 1)

    # Splits dataset into valid and rejected rows
    rejects_df = results_df[reject_mask]
    valid_df = results_df[~reject_mask]

    # Output basic row counts for verification
    print(f"Valid rows: {len(valid_df)}\n")
    print(f"Rejected Rows: {len(rejects_df)}\n")

    # -------------------------------------------------------------------------
    # END of validators, can leave the .to_csv for now
    # -------------------------------------------------------------------------

    # Export cleaned data and rejected data to their respective folders
    valid_df.to_csv("./data/processed/results_processed.csv", index = False)
    rejects_df.to_csv("./data/rejects/results_rejects.csv", index = False)

    # Confirm successful export
    print("Export Complete:")
    print(" - ./data/processed/results_processed.csv")
    print(" - ./data/rejects/results_rejects.csv")