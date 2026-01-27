# TRNG2364-Project1
Everything Project 1 for TRNG2364 Data foundations Started on 01/26/2026


# TRNG2364-Project1 (F1 Data Platform)

Full-stack data engineering project using the Ergast Formula 1 dataset.

## Repo Structure
- `ingestion/`  Python ingestion subsystem (Part 1)
- `infra/`      AWS infrastructure (RDS, S3, etc.)
- `backend/`    API service (later phase)
- `frontend/`   Dashboard UI (later phase)
- `data/`       Local dev data folders (raw/processed/rejects)

## Part 1 Goal (Data Ingestion Subsystem)
- Read CSV/JSON
- Validate + clean
- Remove duplicates
- Load valid rows into PostgreSQL staging table(s)
- Store rejected rows + reasons
- Logging + test coverage (PyTest)

## Dataset
Ergast F1 dataset (bulk CSV export). Primary ingestion target: `results.csv`.