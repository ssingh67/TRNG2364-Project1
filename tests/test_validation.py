import pandas as pd
import pytest

import ingestion.validators as validators

def test_validation_accepts_good_row():
    df = pd.DataFrame([{
        "resultId": 1,
        "raceId": 100,
        "driverId": 200,
        "constructorId": 300,
        "position": 1,
        "points": 25.0
    }])

    required_cols = ["resultId", "raceId", "driverId", "constructorId", "position", "points"]

    if hasattr(validators, "validate_required_columns"):
        validators.validate_required_columns(df, required_cols)
        assert True
        return
    
    if hasattr(validators, "apply_validations"):
        mask = validators.apply_validations(df, {"not_null" : required_cols})
        assert mask.all()
        return
    
    pytest.fail(
        "Could not find a validation entrypoint in ingestion/validators.py."
        "Expected validate_required_columns(df, required_cols) or apply_validations(df, rules)."
    )

def test_validation_rejects_missing_required_column():
    df = pd.DataFrame([{
        "resultId": 1,
        "raceId": 100,
        "driverId": 200,
        "constructorId": 300,
        "position": 1
    }])

    required_cols = ["resultId", "raceId", "driverId", "constructorId", "position", "points"]

    if hasattr(validators, "validate_required_columns"):
        with pytest.raises(Exception):
            validators.validate_required_columns(df, required_cols)
        return
    
    if hasattr(validators, "apply_validations"):
        with pytest.raises(Exception):
            validators.apply_validations(df, {"not_null" : required_cols})
        return
    
    pytest.fail(
        "Could not find a validation entrypoint in ingestion/validators.py."
        "Expected validate_required_columns(df, required_cols) or apply_validations(df, rules)."
    )

def test_split_valid_rejects_by_null_splits_correctly():
    df = pd.DataFrame([
        {"resultId": 1, "raceId": 100, "driverId": 200, "constructorId": 300},
        {"resultId": None, "raceId": 101, "driverId": 201, "constructorId": 301},
        {"resultId": 3, "raceId": None, "driverId": 202, "constructorId": 302},
        {"resultId": 4, "raceId": 103, "driverId": 203, "constructorId": 303},
    ])

    key_cols = ["resultId", "raceId", "driverId", "constructorId"]

    valid_df, rejects_df = validators.split_valid_rejects_by_null(df, key_cols)

    assert len(valid_df) == 2
    assert len(rejects_df) == 2
    assert valid_df["resultId"].isna().sum() == 0
    assert rejects_df["resultId"].isna().sum() == 1

def test_split_valid_rejects_by_null_raises_when_key_missing():
    df = pd.DataFrame([
        {"resultId": 1, "raceId": 100}
    ])

    key_cols = ["resultId", "raceId", "driverId"]

    with pytest.raises(ValueError):
        validators.split_valid_rejects_by_required_not_null(df, key_cols)

def test_split_required_not_null_no_rejects_when_complete():
    if not hasattr(validators, "split_valid_rejects_by_require_not_null"):
        pytest.skip("split_valid_rejects_by_required_not_null not implemented yet")
    
    df = pd.DataFrame([
        {"resultId": 1, "raceId": 100, "points": 25.0},
        {"resultId": 2, "raceId": 101, "points": 0.0},
    ])

    required_not_null = ["resultId", "raceId", "points"]
    valid_df, rejects_df = validators.split_valid_rejects_by_required_not_null(df, required_not_null)

    assert len(valid_df) == 2
    assert len(rejects_df) == 0


def test_split_required_not_null_rejects_rows_with_nulls():
    if not hasattr(validators, "split_valid_rejects_by_required_not_null"):
        pytest.skip("split_valid_rejects_by_required_not_null not implemented yet")

    df = pd.DataFrame([
        {"resultId": 1, "raceId": 100, "points": 25.0},
        {"resultId": 2, "raceId": 101, "points": None},  # should be rejected
        {"resultId": None, "raceId": 102, "points": 5.0},  # should be rejected
    ])

    required_not_null = ["resultId", "raceId", "points"]
    valid_df, rejects_df = validators.split_valid_rejects_by_required_not_null(df, required_not_null)

    assert len(valid_df) == 1
    assert len(rejects_df) == 2
    # sanity: rejects should contain at least one null in required columns
    assert rejects_df[required_not_null].isna().any(axis=1).all()


def test_split_required_not_null_raises_when_column_missing():
    if not hasattr(validators, "split_valid_rejects_by_required_not_null"):
        pytest.skip("split_valid_rejects_by_required_not_null not implemented yet")

    df = pd.DataFrame([{"resultId": 1, "raceId": 100}])  # points missing
    required_not_null = ["resultId", "raceId", "points"]

    with pytest.raises(ValueError):
        validators.split_valid_rejects_by_required_not_null(df, required_not_null)