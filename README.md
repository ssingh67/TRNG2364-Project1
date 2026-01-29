# TRNG2364-Project1 (F1 Data Platform)

Full-stack data engineering project using the Ergast Formula 1 dataset.

## Repository Structure
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