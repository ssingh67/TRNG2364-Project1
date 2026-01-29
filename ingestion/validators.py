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


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    """
    Check that all required columns exist in the DataFrame.
    Returns a list of missing columns (empty list if none are missing).
    """
    return [col for col in required_columns if col not in df.columns]


def split_valid_rejects_by_null(
    df: pd.DataFrame, key_columns: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a DataFrame into valid and rejected rows based on null values
    in key columns. Any row with a null in ANY key column is rejected.
    Returns (valid_df, rejects_df).
    """
    reject_mask = df[key_columns].isna().any(axis=1)

    valid_df = df[~reject_mask].copy()
    rejects_df = df[reject_mask].copy()

    return valid_df, rejects_df
