# PersonalDataAggregationPipeline — Project Instructions

## What this project does
Personal ELT pipeline aggregating data from online services into a local DuckDB database, transformed with dbt Core, scheduled via GitHub Actions.

## Stack
- **Language**: Python (extractors)
- **Database**: DuckDB — local file at `data/personal_data.duckdb`
- **Transform**: dbt Core with `dbt-duckdb` adapter
- **Scheduling**: GitHub Actions daily cron

## Architecture
- `src/extractors/` — one Python script per API source
- Raw data lands in DuckDB `raw` schema
- dbt `staging` models lightly clean raw tables
- dbt `marts` models produce final analytical tables

## Data Sources
- Steam (in progress — first source)
- Others to be added later (GitHub, Spotify, etc.)

## Key paths
- DuckDB file: `data/personal_data.duckdb` (gitignored)
- dbt project root: `dbt/`
- dbt profiles: `dbt/profiles.yml`
- Env vars: `.env` (gitignored), template at `config/.env.example`

## Python version
- Venv **must** use Python 3.12 — dbt-core is incompatible with Python 3.14 (Pydantic v1 dependency)
- Create venv with: `py -3.12 -m venv venv`

## Notes
- Never commit `.env` or the `.duckdb` file
- Each extractor writes to a raw table in DuckDB, named `raw.<source>_<entity>`
- dbt handles all transforms — do not transform data inside extractor scripts

## Plan maintenance
- `plan.md` is the source of truth for project progress
- **Update `plan.md` at the end of every session**: tick off completed items and add a row to the Status Log with the date and a summary of what was done
- If new work is agreed mid-session, add it to the relevant phase (or create a new phase) before starting
