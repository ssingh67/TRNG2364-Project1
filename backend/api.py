from __future__ import annotations

import math
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from backend.db import get_conn

app = FastAPI(title="TRNG2364 Project1 API", version="0.1")

# Dev-friendly CORS (tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STAGING_SCHEMA = "staging"


def _get_staging_tables(conn) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """,
            (STAGING_SCHEMA,),
        )
        return [r[0] for r in cur.fetchall()]


def _get_table_columns(conn, table: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
            """,
            (STAGING_SCHEMA, table),
        )
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            raise HTTPException(status_code=404, detail=f"Unknown table: {table}")
        return cols


@app.get("/api/tables")
def list_tables() -> dict[str, Any]:
    conn = get_conn()
    try:
        tables = _get_staging_tables(conn)
        return {"schema": STAGING_SCHEMA, "tables": tables}
    finally:
        conn.close()


@app.get("/api/tables/{table}")
def get_table_data(
    table: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
    search: str = Query("", max_length=200),
) -> dict[str, Any]:
    conn = get_conn()
    try:
        # Validate table exists in staging
        tables = set(_get_staging_tables(conn))
        if table not in tables:
            raise HTTPException(status_code=404, detail=f"Unknown table: {table}")

        cols = _get_table_columns(conn, table)

        where_sql = sql.SQL("")
        params: list[Any] = []

        # Simple "search across all columns" (CAST to text + ILIKE)
        if search:
            like = f"%{search}%"
            or_parts = [
                sql.SQL("CAST({c} AS TEXT) ILIKE %s").format(c=sql.Identifier(c))
                for c in cols
            ]
            where_sql = sql.SQL("WHERE ") + sql.SQL(" OR ").join(or_parts)
            params.extend([like] * len(cols))

        # Count total
        with conn.cursor() as cur:
            count_q = sql.SQL("SELECT COUNT(*) FROM {s}.{t} ").format(
                s=sql.Identifier(STAGING_SCHEMA),
                t=sql.Identifier(table),
            ) + where_sql
            cur.execute(count_q, params)
            total_rows = cur.fetchone()[0]

        total_pages = max(1, math.ceil(total_rows / page_size))
        offset = (page - 1) * page_size

        # Fetch page
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            data_q = (
                sql.SQL("SELECT * FROM {s}.{t} ").format(
                    s=sql.Identifier(STAGING_SCHEMA),
                    t=sql.Identifier(table),
                )
                + where_sql
                + sql.SQL(" ORDER BY 1 ASC LIMIT %s OFFSET %s")
            )
            cur.execute(data_q, params + [page_size, offset])
            rows = cur.fetchall()

        return {
            "schema": STAGING_SCHEMA,
            "table": table,
            "page": page,
            "page_size": page_size,
            "total_rows": total_rows,
            "total_pages": total_pages,
            "columns": cols,
            "rows": rows,
        }
    finally:
        conn.close()
