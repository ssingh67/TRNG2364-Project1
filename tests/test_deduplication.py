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
        out = cleaners.remove_duplicates(df, key_columns)
        assert len(out) == 1
        return
    
    pytest.fail(
        "No deduplication function found in ingestion/cleaners.py"
        "Add a small helper like deduplicate(df, key_columns) that returns df.drop_duplicates(subset = key_columns)"
    )

def test_deduplication_no_change_when_no_duplicates():
    key_columns = ["resultId"]

    df = pd.DataFrame([
        {"resultId": 1, "points": 25.0},
        {"resultId": 2, "points": 18.0},
        {"resultId": 3, "points": 0.0},
    ])

    if hasattr(cleaners, "deduplicate"):
        out = cleaners.deduplicate(df, key_columns)
        assert len(out) == 3
        assert set(out["resultId"].tolist()) == {1, 2, 3}
        return

    if hasattr(cleaners, "remove_duplicates"):
        out = cleaners.remove_duplicates(df, key_columns)
        assert len(out) == 3
        return

    pytest.fail("No deduplication function found in ingestion/cleaners.py")

def test_deduplication_raises_when_key_column_missing():
    key_columns = ["resultId"]

    df = pd.DataFrame([
        {"raceId": 100, "points": 25.0},
        {"raceId": 101, "points": 18.0},
    ])

    if hasattr(cleaners, "deduplicate"):
        with pytest.raises(Exception):
            cleaners.deduplicate(df, key_columns)
        return

    if hasattr(cleaners, "remove_duplicates"):
        with pytest.raises(Exception):
            cleaners.remove_duplicates(df, key_columns)
        return

    pytest.fail("No deduplication function found in ingestion/cleaners.py")

def test_deduplication_collapses_same_key_even_if_other_columns_differ():
    key_columns = ["resultId"]

    df = pd.DataFrame([
        {"resultId": 1, "points": 25.0},
        {"resultId": 1, "points": 18.0},
        {"resultId": 2, "points": 10.0},
    ])

    if hasattr(cleaners, "deduplicate"):
        out = cleaners.deduplicate(df, key_columns)
        assert len(out) == 2
        assert set(out["resultId"].tolist()) == {1, 2}
        return

    if hasattr(cleaners, "remove_duplicates"):
        out = cleaners.remove_duplicates(df, key_columns)
        assert len(out) == 2
        return

    pytest.fail("No deduplication function found in ingestion/cleaners.py")