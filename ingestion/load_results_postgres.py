import pandas as pd
from backend.db import get_conn


def load_results_to_postgres(csv_path: str):
    """
    Load processed results into PostgreSQL staging table.
    """
    df = pd.read_csv(csv_path)

    insert_sql = """
        INSERT INTO stg_results (
            result_id,
            race_id,
            driver_id,
            constructor_id,
            position,
            points
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute(
                    insert_sql,
                    (
                        row["resultId"],
                        row["raceId"],
                        row["driverId"],
                        row["constructorId"],
                        row["position"],
                        row["points"],
                    )
                )
        conn.commit()

    print(f"Inserted {len(df)} rows into stg_results")
