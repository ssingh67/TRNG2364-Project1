import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    """
    Create and return a new PostgreSQL connection using environment variables.
    """
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=int(os.getenv("PGPORT")),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )
