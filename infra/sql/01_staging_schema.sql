CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.stg_constructors (
  constructor_id  INTEGER PRIMARY KEY,
  constructor_ref TEXT,
  name            TEXT,
  nationality     TEXT,
  url             TEXT,
  ingested_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.stg_drivers (
  driver_id     INTEGER PRIMARY KEY,
  driver_ref    TEXT,
  number        INTEGER,
  code          TEXT,
  forename      TEXT,
  surname       TEXT,
  dob           DATE,
  nationality   TEXT,
  url           TEXT,
  ingested_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.stg_races (
  race_id      INTEGER PRIMARY KEY,
  year         INTEGER,
  round        INTEGER,
  circuit_id   INTEGER,
  name         TEXT,
  race_date    DATE,
  race_time    TIME,
  url          TEXT,
  ingested_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.stg_results (
  result_id      INTEGER PRIMARY KEY,
  race_id        INTEGER NOT NULL,
  driver_id      INTEGER NOT NULL,
  constructor_id INTEGER NOT NULL,
  position       INTEGER,
  points         NUMERIC(6,2),
  ingested_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stg_results_race_id        ON staging.stg_results (race_id);
CREATE INDEX IF NOT EXISTS idx_stg_results_driver_id      ON staging.stg_results (driver_id);
CREATE INDEX IF NOT EXISTS idx_stg_results_constructor_id ON staging.stg_results (constructor_id);
