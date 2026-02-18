# F1 Data Platform

A full-stack cloud-based data engineering platform built on the Ergast Formula 1 dataset. The system implements a complete end-to-end pipeline including configurable data ingestion, PostgreSQL staging and normalized core schemas, a FastAPI analytics service, and a dynamic React dashboard UI.

The platform is deployed on AWS RDS and demonstrates modern data engineering architecture, schema design, API development, and frontend integration.

---

## Architecture Overview

Raw CSV Dataset (Ergast F1)
        ↓
Config-Driven Ingestion Pipeline (Python)
        ↓
Staging Schema (PostgreSQL - AWS RDS)
        ↓
Normalized Core Schema
        ↓
FastAPI Backend (Analytics Endpoints)
        ↓
React Dashboard UI

This architecture separates ingestion, transformation, analytics, and presentation layers for maintainability and scalability.

---

## Tech Stack

### Backend & Data Engineering
- Python
- pandas
- FastAPI
- PostgreSQL
- psycopg2
- SQLAlchemy
- PyYAML
- python-dotenv

### Frontend
- React (Vite)
- React Router
- Modern CSS UI styling

### Infrastructure
- AWS RDS (PostgreSQL)
- Security Groups with IP allowlisting

---

## Repository Structure
- `ingestion/` – Config-driven ingestion pipeline  
- `backend/` – FastAPI service layer  
- `frontend/` – React dashboard UI  
- `infra/` – Infrastructure configuration  
- `data/` – Raw, processed, rejects, logs  

---

## Database Design

The platform uses a two-layer relational model.

### Staging Schema (`staging`)

Raw validated data loaded directly from ingestion with minimal transformation

Tables:
- `stg_drivers`
- `stg_constructors`
- `stg_races`
- `stg_results`

Purpose:
- Safe loading zone
- Preserve ingested structure
- Isolate raw data from analytics logic

### Core Schema (`core`)

Normalized relational model powering analytics and API queries

Tables:
- `drivers`
- `constructors`
- `races`
- `results`

Purpose:
- Enforce foreign key relationships
- Enable aggregation queries
- Support analytics endpoints

The database is hosted on AWS RDS (PostgreSQL).

Separate roles are used for administrative and application-level access.

---

## Data Ingestion

The ingestion subsystem reads raw CSV files, validates and cleans records, and prepares structured outputs for database loading.

### What It Does
- Reads dataset files (config-driven)
- Validates schema and required fields
- Cleans and standardizes data
- Removes duplicate records
- Separates valid and rejected rows
- Writes deterministic outputs
- Loads validated data into PostgreSQL staging tables

All ingestion behavior is controlled via

`ingestion/config.yaml`

No code changes are required to adjust file paths, validation rules, or deduplication keys

### Running Ingestion

### Windows (PowerShell)

```powershell
python run_ingestion.py
```

### macOS / Linux

```bash
python3 run_ingestion.py
```

Outputs:
- `data/processed/` → cleaned data
- `data/rejects/` → rejected records
- `data/logs/` → ingestion logs

---

## API Service

The FastAPI backend exposes validated and normalized data through REST endpoints

### Available Endpoints

| Endpoint | Description |
|----------|------------|
| `/api/tables` | List available tables |
| `/api/tables/{table}` | Paginated table data |
| `/api/core/leaderboard` | Top drivers by total points |
| `/api/core/constructors?year=YYYY` | Constructor standings for a year |
| `/api/core/drivers/{driver_id}/stats` | Driver career statistics |
| `/docs` | Interactive Swagger documentation |

### Running the API

### Windows (PowerShell)
```powershell
python -m uvicorn backend.api:app --reload --port 8000
```

### macOS / Linux
```bash
python3 -m uvicorn backend.api:app --reload --port 8000
```

Open:
`http://127.0.0.1:8000/docs`

---

## Frontend Dashboard

The React dashboard provides interactive exploration of normalized core schema data through analytics endpoints exposed by the FastAPI backend.

### Features
- Dynamic table discovery
- Pagination
- Search
- Driver statistics lookup
- Constructor standing by year
- Leaderboard analytics
- Schema-agnostic table rendering

## Frontend Setup

### Windows (PowerShell) / macOS / Linux (Bash)
```bash
cd frontend
npm install
```

Create `frontend/.env`:
```ini
VITE_API_BASE = http://127.0.0.1:8000
```

Run:
### Windows (PowerShell) / macOS / Linux (Bash)
```bash
npm run dev
```

Open:
```
http://127.0.0.1:5173
```


## Running the Full Application

Open two terminals

### Terminal 1 - Backend

### Windows (PowerShell)
```powershell
python -m uvicorn backend.api:app --reload --port 8000
```

### macOS / Linux
```bash
python3 -m uvicorn backend.api:app --reload --port 8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Then visit:
```
http://localhost:5173
```

---

## Environment Setup

### Python Virtual Environment

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Deactivate when finished:
```
deactivate
```

---

## AWS Deployment Notes

- Database hosted on AWS RDS (PostgreSQL)
- Security Group inbound rules restrict access by IP (/32)
- Separate roles for ingestion and API access
- Environment variables managed via `.env`

---

## Dataset

Source: Ergast Formula 1 bulk CSV export (1950 - 2024)

Primary ingested datasets:
- `drivers.csv`
- `constructors.csv`
- `races.csv`
- `results.csv`

The dataset contains over 2,000 non-synthetic records and supports meaningful relational analytics

---

## Project Highlights
- Config-driven ingestion architecture
- Modular validation and cleaning pipeline
- Two-layer relational schema design
- Cloud-hosted PostgreSQL deployment
- RESTful analytics service
- Dynamic Frontend integration
- Clean Separation of ingestion, transformation, and presentation layers

---

## Troubleshooting

| Issue | Cause |
|----------|------------|
| "Failed to fetch" | Backend not running |
| No tables visible | Ingestion not executed |
| Empty analytics results | Year outside dataset range |
| Database connection refused | AWS Security Group or `.env` misconfigured |
| API works but UI empty | Restart frontend after editing `.env` |