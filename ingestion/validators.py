"""
Validation utilities for the ingestion subsystem.

This module is intended to hold:
- Required column validation logic
- Row-level validation (e.g., null checks)
- Any reusable validation rules shared across datasets

NOTE:
- Ingestion files should CALL these functions, not reimplement validation
"""

import pandas as pd


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """
    Ensure all required columns exist in the DataFrame.
    Raises ValueError if any required columns are missing.
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Required columns missing from DataFrame: {missing}")

def split_valid_rejects_by_null(
    df: pd.DataFrame, key_columns: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a DataFrame into valid and rejected rows based on null values
    in key columns. Any row with a null in ANY key column is rejected.
    Returns (valid_df, rejects_df).
    """
    missing_keys = [c for c in key_columns if c not in df.columns]

    if missing_keys:
        raise ValueError(f"Key columns missing from DataFrame: {missing_keys}")

    reject_mask = df[key_columns].isna().any(axis=1)

    valid_df = df[~reject_mask].copy()
    rejects_df = df[reject_mask].copy()

    return valid_df, rejects_df

def split_valid_rejects_by_required_not_null(
        df: pd.DataFrame, required_not_null_columns: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a DataFrame inot valid and rejected rows based on null values in required_not_null_columns. Any row with a null in ANY required column is rejected. Returns (valid_df, rejects_df)
    """

    missing_cols = [c for c in required_not_null_columns if c not in df.columns]

    if missing_cols:
        raise ValueError(f"Required-not-null columns missing from DataFrame: {missing_cols}")
    
    reject_mask = df[required_not_null_columns].isna().any(axis = 1)

    valid_df = df[~reject_mask].copy()
    rejects_df = df[reject_mask].copy()

    return valid_df, rejects_df