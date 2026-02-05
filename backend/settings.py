"""
Application settings and configuration.

This file is responsible for:
- Loading environment variables
- Defining database connection settings
- Centralizing configuration so it is NOT duplicated across files

Nothing in here should perform business logic.

please configure your .env file to connect to the database
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into environment
# This allows os.getenv(...) to work everywhere
load_dotenv()

# -------------------------------------------------------------------
# Database Settings
# -------------------------------------------------------------------

# PostgreSQL host (localhost for local development)
PGHOST = os.getenv("PGHOST", "localhost")

# PostgreSQL port (default is 5432)
PGPORT = int(os.getenv("PGPORT", 5432))

# PostgreSQL database name
PGDATABASE = os.getenv("PGDATABASE")

# PostgreSQL user
PGUSER = os.getenv("PGUSER")

# PostgreSQL password
PGPASSWORD = os.getenv("PGPASSWORD")

# Safety check — fail fast if something important is missing
REQUIRED_DB_VARS = {
    "PGDATABASE": PGDATABASE,
    "PGUSER": PGUSER,
    "PGPASSWORD": PGPASSWORD,
}

missing = [key for key, value in REQUIRED_DB_VARS.items() if not value]

if missing:
    raise RuntimeError(
        f"Missing required database environment variables: {', '.join(missing)}"
    )

# -------------------------------------------------------------------
# Database Schema / Table Names
# -------------------------------------------------------------------

# Schema used for ingestion & staging
STAGING_SCHEMA = "staging"

# Staging table for F1 results
STG_RESULTS_TABLE = "stg_results"

# Fully qualified table name (schema.table)
STG_RESULTS_FULL_TABLE = f"{STAGING_SCHEMA}.{STG_RESULTS_TABLE}"

# -------------------------------------------------------------------
# Application Settings (future-proofing)
# -------------------------------------------------------------------

# Whether the app is running in debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Application name (useful for logs later)
APP_NAME = "TRNG2364 Project 1 Backend"
