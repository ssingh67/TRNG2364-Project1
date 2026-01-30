# TRNG2364-Project1 (F1 Data Platform)

Full-stack data engineering project using the Ergast Formula 1 dataset.

## Repository Structure
- `ingestion/`  Python ingestion subsystem (Part 1)
- `infra/`      AWS infrastructure (RDS, S3, etc.)
- `backend/`    API service (later phase)
- `frontend/`   Dashboard UI (later phase)
- `data/`       Local dev data folders (raw/processed/rejects)

## Part 1 Goal (Data Ingestion Subsystem)

The Data Ingestion Subsystem is responsible for reading raw dataset files, validating and cleaning the data, and producing standardized outputs that downstream components can safely depend on.

### What ingestion does
- Read raw data from CSV (config-driven)
- Validate schema and row-level data
- Cleans and standardizes values
- Removes duplicate records
- Separates valid and rejected rows
- Write deterministic outputs for downstream use

### How to run
```powershell
python run_ingestion.py
```

## Configuration

All ingestion behavior is controlled by:
```
ingestion/config.yaml
```

The configuration defines:
- Source file paths
- Required columns
- Validation rules
- Deduplication keys
- Output locations

No code changes are required to adjust ingestion behavior - only config updates.

### Outputs
- ```data/processed/``` → validated and cleaned data
- ```data/rejects/``` → records that failed validation
- ```data/logs/``` → reserved for ingestion logs (later phase)

This ingestion layer is stable and safe to depend on for later phases (database loading, APIs, and AWS development)

## Dataset
Ergast F1 dataset (bulk CSV export). Primary ingestion target: `results.csv`.

## Python Dependencies & Environment Setup

### Virtual Environment

This project uses Python virtual environment to isolate dependencies and ensure reproducibility.

Create the virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment
```powershell
.\venv\Scripts\Activate
```

Deactivate when finished
```powershell
deactivate
```

### Python Dependencies

Dependencies are managed using `pip` and tracked in `requirements.txt`.

The following core packages are used for **Part 1 - Data Ingestion Subsystem**:

| Package | Purpose |
| --- | --- |
| pandas | Reading and processing CSV/JSON data |
| numpy | Numerical operations (pandas dependency) |
| SQLAlchemy | Database abstraction and PostgreSQL integration |
| psycopg2-binary | PostgreSQL database driver |
| pydantic | Data validation and schema enforcement |
| PyYAML | Configuration management (YAML-based settings) |
| python-dotenv | Environment variable and secrets management |
| pytest | Unit testing framework |

Some additional packages (e.g., `six`, `greenlet`, `pluggy`) are installed automatically as dependencies of the core libraries.

### Installing Dependencies

All dependencies and their versions are locked in `requirements.txt`.

To install dependencies in a fresh environment:

```powershell
pip install -r requirements.txt
```

To generate or update the dependency list:

```powershell
pip freeze > requirements.txt
```