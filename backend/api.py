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

DATA_SCHEMA = "core"


def _get_schema_tables(conn, schema: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """,
            (schema,),
        )
        return [r[0] for r in cur.fetchall()]


def _get_table_columns(conn, schema: str, table: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
            """,
            (schema, table),
        )
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            raise HTTPException(status_code = 404, detail = f"Unknown table: {schema}.{table}")
        return cols


@app.get("/api/tables")
def list_tables() -> dict[str, Any]:
    conn = get_conn()
    try:
        tables = _get_schema_tables(conn, DATA_SCHEMA)
        return {"schema": DATA_SCHEMA, "tables": tables}
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
        tables = set(_get_schema_tables(conn, DATA_SCHEMA))
        if table not in tables:
            raise HTTPException(status_code=404, detail=f"Unknown table: {table}")

        cols = _get_table_columns(conn, DATA_SCHEMA, table)

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
                s=sql.Identifier(DATA_SCHEMA),
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
                    s=sql.Identifier(DATA_SCHEMA),
                    t=sql.Identifier(table),
                )
                + where_sql
                + sql.SQL(" ORDER BY 1 ASC LIMIT %s OFFSET %s")
            )
            cur.execute(data_q, params + [page_size, offset])
            rows = cur.fetchall()

        return {
            "schema": DATA_SCHEMA,
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

@app.get("/api/core/leaderboard")
def get_leaderboard(limit: int = Query(10, ge = 1, le = 50)) -> list[dict[str, Any]]:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory = RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    d.driver_id,
                    d.forename || ' ' || d.surname AS driver_name,
                    SUM(r.points) AS total_points
                FROM core.results r
                JOIN core.drivers d ON d.driver_id = r.driver_id
                GROUP BY d.driver_id, driver_name
                ORDER BY total_points DESC
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()
    finally:
        conn.close()

@app.get("/api/core/constructors")
def get_constructors_by_year(year: int = Query(..., ge = 1950)) -> list[dict[str, Any]]:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory = RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    c.constructor_id,
                    c.name AS constructor_name,
                    SUM(r.points) AS total_points
                FROM core.results r
                JOIN core.races ra ON ra.race_id = r.race_id
                JOIN core.constructors c ON c.constructor_id = r.constructor_id
                WHERE ra.year = %s
                GROUP BY c.constructor_id, constructor_name
                ORDER BY total_points DESC;
                """,
                (year,),
            )
            return cur.fetchall()
    finally:
        conn.close()

@app.get("/api/core/drivers/{driver_id}/stats")
def get_driver_stats(driver_id: int) -> dict[str, Any]:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory = RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    d.driver_id,
                    d.forename || ' ' || d.surname AS driver_name,
                    COUNT(*) AS races,
                    SUM(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins,
                    SUM(CASE WHEN r.position IN (1, 2, 3) THEN 1 ELSE 0 END) AS podiums,
                    SUM(r.points) AS total_points
                FROM core.results r
                JOIN core.drivers d ON d.driver_id = r.driver_id
                WHERE d.driver_id = %s
                GROUP BY d.driver_id, driver_name;
                """,
                (driver_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code = 404, detail = "Driver not found")
            return row
    finally:
        conn.close()
