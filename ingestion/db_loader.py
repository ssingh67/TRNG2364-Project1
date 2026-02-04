from __future__ import annotations

from typing import Iterable, List, Sequence
import pandas as pd
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import execute_batch

def load_results_to_postgres(
        df: pd.DataFrame,
        conn: PgConnection,
        table_name: str,
        columns: Sequence[str],
        page_size: int = 1000,
) -> int:
    if df is None or df.empty:
        return 0
    
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame missing required DB insert columns: {missing}")
    
    col_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})"

    records: List[tuple] = [
        tuple(row[c] for c in columns) for _, row in df.iterrows()
    ]

    try:
        with conn.cursor() as cur:
            execute_batch(cur, insert_sql, records, page_size = page_size)
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return len(records)