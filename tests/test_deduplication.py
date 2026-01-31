import pandas as pd
import pytest

import ingestion.cleaners as cleaners

def test_deduplication_removes_duplicates_on_key_columns():
    key_columns = ["resultId", "raceId", "driverId", "constructorId"]

    df = pd.DataFrame([
        {"resultId": 1, "raceId": 100, "driverId": 200, "constructorId": 300, "position": 1, "points": 25.0},
        {"resultId": 1, "raceId": 100, "driverId": 200, "constructorId": 300, "position": 1, "points": 25.0},
    ])

    if hasattr(cleaners, "deduplicate"):
        out = cleaners.deduplicate(df, key_columns)
        assert len(out) == 1
        return
    
    if hasattr(cleaners, "remove_duplicates"):
        out = cleaners.remove_duplciates(df, key_columns)
        assert len(out) == 1
        return
    
    pytest.fail(
        "No deduplication function found in ingestion/cleaners.py"
        "Add a small helper like deduplicate(df, key_columns) that returns df.drop_duplicates(subset = key_columns)"
    )