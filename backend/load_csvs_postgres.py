import pandas as pd
import numpy as np
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import execute_batch
from typing import Sequence, List


def load_dataframe_to_postgres(
        df: pd.DataFrame,
        conn: PgConnection,
        table_name: str,
        columns: Sequence[str],
        page_size: int = 100,
        truncate_first: bool = False
) -> int:
    """
    Load a DataFrame inot a PostgreSQL table using batch inserts.
    """
    if df is None or df.empty:
        return 0
    
    # Converting NaN/NaT to Python None so psycopg2 inserts NULLs
    df = df.replace({np.nan: None})
    
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame missing required DB columns: {missing}")
    
    col_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})"

    records: List[tuple] = [
        tuple(row[c] for c in columns) for _, row in df.iterrows()
    ]

    try:
        with conn.cursor() as cur:
            if truncate_first:
                cur.execute(f"TRUNCATE TABLE {table_name}")
            
            execute_batch(cur, insert_sql, records, page_size = page_size)
        
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return len(records)
