# Personal Data Aggregation Pipeline

A personal ELT pipeline that pulls data from various online services, loads it into a local DuckDB database, and transforms it with dbt Core. Scheduled via GitHub Actions.

## Stack

- **Extract & Load**: Python (per-source extractor scripts)
- **Database**: DuckDB (local `.duckdb` file)
- **Transform**: dbt Core with `dbt-duckdb` adapter
- **Schedule**: GitHub Actions (daily cron)

## Architecture

```
API Sources  →  Python extractors  →  DuckDB (raw schema)  →  dbt models  →  DuckDB (marts schema)
```

Data sources planned:
- Steam (games, playtime, achievements)

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
├── data/                    # Local DuckDB file (gitignored)
├── .github/
│   └── workflows/
│       └── pipeline.yml     # Daily cron job
├── config/
│   └── .env.example
├── requirements.txt
└── .gitignore
```

## Setup

1. Create and activate virtual environment: `python -m venv venv && venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config/.env.example` to `.env` and fill in API credentials
4. Run an extractor: `python src/extractors/steam.py`
5. Run dbt transforms: `cd dbt && dbt run`

## Environment Variables

See `config/.env.example` for required variables.
