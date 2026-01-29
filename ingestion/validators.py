"""
Validation utilities for the ingestion subsystem.

This module is intended to hold:
- Required column validation logic
- Row-level validation (e.g., null checks)
- Any reusable validation rules shared across datasets

NOTE:
- Logic currently lives in read_results.py
- That logic should be refactored into functions here (I have comments about what needs to move into here)
- Ingestion files should CALL these functions, not reimplement validation
"""

# These are the placeholder functions:
def validate_required_columns(df, require_columns):
    """
    Check that all required columns exist in the DataFrame
    Then returns a list of missing columns (empty list if none are missing)
    """
    pass

def split_valid_rejects_by_null(df, key_columns):
    """
    Split a DataFrame into valid and rejected rows based on null values in key columns (there should not be any null values)
    Then return (valid_df, rejects_df)
    """
    pass