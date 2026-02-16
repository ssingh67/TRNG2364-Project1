-- 1) Core schema
CREATE SCHEMA IF NOT EXISTS core;

-- 2) Core tables (no ingested_at; core is “cleaned/curated”)
CREATE TABLE IF NOT EXISTS core.constructors (
  constructor_id  INTEGER PRIMARY KEY,
  constructor_ref TEXT,
  name            TEXT,
  nationality     TEXT,
  url             TEXT
);

CREATE TABLE IF NOT EXISTS core.drivers (
  driver_id     INTEGER PRIMARY KEY,
  driver_ref    TEXT,
  number        INTEGER,
  code          TEXT,
  forename      TEXT,
  surname       TEXT,
  dob           DATE,
  nationality   TEXT,
  url           TEXT
);

CREATE TABLE IF NOT EXISTS core.races (
  race_id      INTEGER PRIMARY KEY,
  year         INTEGER,
  round        INTEGER,
  circuit_id   INTEGER,
  name         TEXT,
  race_date    DATE,
  race_time    TIME,
  url          TEXT
);

CREATE TABLE IF NOT EXISTS core.results (
  result_id      INTEGER PRIMARY KEY,
  race_id        INTEGER NOT NULL,
  driver_id      INTEGER NOT NULL,
  constructor_id INTEGER NOT NULL,
  position       INTEGER,
  points         NUMERIC(6,2)
);

-- 3) Load dimensions first (idempotent)
INSERT INTO core.constructors (constructor_id, constructor_ref, name, nationality, url)
SELECT s.constructor_id, s.constructor_ref, s.name, s.nationality, s.url
FROM staging.stg_constructors s
ON CONFLICT (constructor_id) DO UPDATE
SET constructor_ref = EXCLUDED.constructor_ref,
    name            = EXCLUDED.name,
    nationality     = EXCLUDED.nationality,
    url             = EXCLUDED.url;

INSERT INTO core.drivers (driver_id, driver_ref, number, code, forename, surname, dob, nationality, url)
SELECT s.driver_id, s.driver_ref, s.number, s.code, s.forename, s.surname, s.dob, s.nationality, s.url
FROM staging.stg_drivers s
ON CONFLICT (driver_id) DO UPDATE
SET driver_ref  = EXCLUDED.driver_ref,
    number      = EXCLUDED.number,
    code        = EXCLUDED.code,
    forename    = EXCLUDED.forename,
    surname     = EXCLUDED.surname,
    dob         = EXCLUDED.dob,
    nationality = EXCLUDED.nationality,
    url         = EXCLUDED.url;

INSERT INTO core.races (race_id, year, round, circuit_id, name, race_date, race_time, url)
SELECT s.race_id, s.year, s.round, s.circuit_id, s.name, s.race_date, s.race_time, s.url
FROM staging.stg_races s
ON CONFLICT (race_id) DO UPDATE
SET year       = EXCLUDED.year,
    round      = EXCLUDED.round,
    circuit_id = EXCLUDED.circuit_id,
    name       = EXCLUDED.name,
    race_date  = EXCLUDED.race_date,
    race_time  = EXCLUDED.race_time,
    url        = EXCLUDED.url;

-- 4) Load fact table (results) after dimensions
INSERT INTO core.results (result_id, race_id, driver_id, constructor_id, position, points)
SELECT s.result_id, s.race_id, s.driver_id, s.constructor_id, s.position, s.points
FROM staging.stg_results s
ON CONFLICT (result_id) DO UPDATE
SET race_id        = EXCLUDED.race_id,
    driver_id      = EXCLUDED.driver_id,
    constructor_id = EXCLUDED.constructor_id,
    position       = EXCLUDED.position,
    points         = EXCLUDED.points;

-- 5) Add indexes + foreign keys (safe “IF NOT EXISTS” pattern via DO blocks)
CREATE INDEX IF NOT EXISTS idx_core_results_race_id        ON core.results (race_id);
CREATE INDEX IF NOT EXISTS idx_core_results_driver_id      ON core.results (driver_id);
CREATE INDEX IF NOT EXISTS idx_core_results_constructor_id ON core.results (constructor_id);

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_core_results_race') THEN
    ALTER TABLE core.results
      ADD CONSTRAINT fk_core_results_race
      FOREIGN KEY (race_id) REFERENCES core.races(race_id);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_core_results_driver') THEN
    ALTER TABLE core.results
      ADD CONSTRAINT fk_core_results_driver
      FOREIGN KEY (driver_id) REFERENCES core.drivers(driver_id);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_core_results_constructor') THEN
    ALTER TABLE core.results
      ADD CONSTRAINT fk_core_results_constructor
      FOREIGN KEY (constructor_id) REFERENCES core.constructors(constructor_id);
  END IF;
END $$;

-- 6) Quick verification
SELECT 'core.constructors' AS table, COUNT(*) AS rows FROM core.constructors
UNION ALL
SELECT 'core.drivers', COUNT(*) FROM core.drivers
UNION ALL
SELECT 'core.races', COUNT(*) FROM core.races
UNION ALL
SELECT 'core.results', COUNT(*) FROM core.results;