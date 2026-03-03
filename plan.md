# Personal Data Aggregation Pipeline — Plan

## Stack
- **Extract & Load**: Python extractor scripts
- **Database**: DuckDB (local file `data/personal_data.duckdb`)
- **Transform**: dbt Core + `dbt-duckdb` adapter
- **Schedule**: GitHub Actions (daily cron)

## Pattern
ELT: extractors write raw data to DuckDB `raw` schema → dbt staging models clean → dbt marts models produce analytical tables.

---

## Phases

### Phase 1 — Project Scaffolding
- [x] Create folder structure (`src/extractors/`, `dbt/`, `data/`, `.github/workflows/`, `config/`)
- [x] Write `requirements.txt` (duckdb, dbt-core, dbt-duckdb, requests, python-dotenv)
- [x] Write `config/.env.example` with placeholder vars
- [x] Update `.gitignore` to include `data/`, `*.duckdb`, dbt artifacts
- [x] Create dbt project files (`dbt/dbt_project.yml`, `dbt/profiles.yml`)
- [x] Create dbt model directories (`models/staging/`, `models/marts/`)
- [x] Install dependencies: `pip install -r requirements.txt`
- [x] Resolve Python 3.14 incompatibility — installed Python 3.12 via winget, rebuilt venv with `py -3.12 -m venv venv`
- [x] Verified `dbt debug` passes (dbt 1.11.6, dbt-duckdb 1.10.1, DuckDB 1.4.4)

### Phase 2 — Steam Extractor
- [x] Write `src/extractors/steam.py`
  - Calls `IPlayerService/GetOwnedGames` — writes to `raw.steam_owned_games`
  - Calls `ISteamUserStats/GetPlayerAchievements` per game — writes to `raw.steam_achievements`
  - Calls `ISteamUser/GetPlayerSummaries` — writes to `raw.steam_profile`
- [x] Steam vars already present in `.env`; removed stale PostgreSQL entries
- [x] Smoke test passed: 686 games, 1 profile, 28 296 achievements loaded

### Phase 3 — dbt Steam Models
- [x] `staging/stg_steam__owned_games.sql` — clean and type-cast raw owned games
- [x] `staging/stg_steam__achievements.sql` — clean raw achievements
- [x] `staging/stg_steam__profile.sql` — clean raw profile
- [x] `marts/steam_games.sql` — games with playtime_hours, last_played_at, achievement stats
- [x] `staging/sources.yml` — defines raw source tables
- [x] `staging/schema.yml` and `marts/schema.yml` — 13 not_null/unique tests
- [x] `macros/generate_schema_name.sql` — schema isolation (staging / marts)
- [x] `dbt run` — 4/4 models OK (0.25s)
- [x] `dbt test` — 13/13 tests PASS

### Phase 4 — GitHub Actions Pipeline
- [ ] Write `.github/workflows/pipeline.yml`
  - Daily cron trigger
  - Steps: checkout → setup Python → install deps → run extractor → run dbt
- [ ] Add `STEAM_API_KEY` and `STEAM_ID` as GitHub Actions secrets
- [ ] Test workflow run manually via `workflow_dispatch`

### Phase 5 — Additional Sources (to be planned when Phase 4 is complete)
Candidates (in rough priority order):
- GitHub (repos, commits, stars)
- Spotify (listening history, top tracks)
- MyAnimeList (watch list, ratings)
- Others TBD

---

## Status Log
| Date | Work completed |
|---|---|
| 2026-03-03 | Project reset; old PostgreSQL/Metabase stack removed |
| 2026-03-03 | Stack decided: Python + DuckDB + dbt Core + GitHub Actions |
| 2026-03-03 | Phase 1 complete: folders, requirements.txt, .env.example, .gitignore, dbt_project.yml, profiles.yml, deps installed, dbt debug passing |
| 2026-03-03 | Note: project venv must use Python 3.12 — dbt-core is incompatible with Python 3.14 (Pydantic v1 limitation) |
| 2026-03-03 | Phase 2 complete: Steam extractor written and smoke-tested (686 games, 1 profile, 28 296 achievements) |
| 2026-03-03 | Phase 3 complete: dbt staging views + steam_games mart table, 13/13 tests passing |
