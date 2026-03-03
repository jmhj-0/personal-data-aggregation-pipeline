# Personal Data Aggregation Pipeline

A personal ELT pipeline that pulls data from various online services, loads it into a local DuckDB database, transforms it with dbt Core, and visualises it with an Evidence dashboard. Scheduled via GitHub Actions.

## Stack

- **Extract & Load**: Python (per-source extractor scripts)
- **Database**: DuckDB (local `.duckdb` file)
- **Transform**: dbt Core with `dbt-duckdb` adapter
- **Dashboard**: Evidence (local dev server)
- **Schedule**: GitHub Actions (daily cron, 02:00 UTC)

## Architecture

```
API Sources  →  Python extractors  →  DuckDB (raw)  →  dbt  →  DuckDB (marts)  →  Evidence dashboard
```

## Data Sources

| Source | Status | Tables |
|---|---|---|
| Steam | Live | owned games, profile, achievements |

## Project Structure

```
PersonalDataAggregationPipeline/
├── src/
│   └── extractors/          # One script per API source
├── dbt/                     # dbt project
│   ├── models/
│   │   ├── staging/         # Light cleaning of raw tables
│   │   └── marts/           # Final analytical models
│   ├── dbt_project.yml
│   └── profiles.yml
├── dashboard/               # Evidence dashboard
│   ├── pages/               # Markdown report pages
│   └── sources/             # DuckDB source config + SQL queries
├── data/                    # Local DuckDB file (gitignored)
├── .github/
│   └── workflows/
│       └── pipeline.yml     # Daily cron job
├── config/
│   └── .env.example
└── requirements.txt
```

## Setup

> **Requires Python 3.12.** dbt-core is incompatible with Python 3.14 due to a Pydantic v1 dependency.

### Pipeline

1. Install Python 3.12 if needed: `winget install Python.Python.3.12`
2. Create virtual environment: `py -3.12 -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `config/.env.example` to `.env` and fill in API credentials
6. Run an extractor: `python src/extractors/steam.py`
7. Run dbt: `cd dbt && dbt run --profiles-dir . && dbt test --profiles-dir .`

### Dashboard

1. Install Node.js 18+ if needed
2. `cd dashboard && npm install`
3. `npm run sources` (pulls data from DuckDB into Evidence cache)
4. `npm run dev` (starts dev server at http://localhost:3000)

> Re-run `npm run sources` after each pipeline run to refresh the dashboard data.

## Environment Variables

See `config/.env.example` for required variables.

## GitHub Actions

The pipeline runs daily at 02:00 UTC. Required secrets: `STEAM_API_KEY`, `STEAM_ID`.

The built DuckDB file is uploaded as a workflow artifact (7-day retention) after each run.
