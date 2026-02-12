from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI(title="ETL Data API")

# allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data/processed")


def load_table(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}_processed.csv"
    if not path.exists():
        raise FileNotFoundError(f"{name} not found")
    return pd.read_csv(path)


@app.get("/api/tables")
def list_tables():
    tables = [
        p.name.replace("_processed.csv", "")
        for p in DATA_DIR.glob("*_processed.csv")
    ]
    return {"tables": tables}


@app.get("/api/tables/{table}")
def get_table(
    table: str,
    page: int = 1,
    page_size: int = 25,
    search: str = Query(default="")
):
    df = load_table(table)

    # simple search across all columns
    if search:
        mask = df.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False)
        ).any(axis=1)
        df = df[mask]

    total_rows = len(df)

    start = (page - 1) * page_size
    end = start + page_size

    df_page = df.iloc[start:end]

    return {
        "table": table,
        "columns": list(df_page.columns),
        "rows": df_page.to_dict(orient="records"),
        "page": page,
        "page_size": page_size,
        "total_rows": total_rows
    }
