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