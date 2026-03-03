# Personal Data Aggregation Pipeline

A personal ELT pipeline that pulls data from various online services, loads it into a local DuckDB database, transforms it with dbt Core, and publishes it as an Evidence dashboard at **[jmhj.info](https://jmhj.info)**. Runs automatically every day via GitHub Actions.

## Stack

- **Extract & Load**: Python (one script per source)
- **Database**: DuckDB (local `.duckdb` file)
- **Transform**: dbt Core + `dbt-duckdb` adapter
- **Dashboard**: Evidence — live at [jmhj.info](https://jmhj.info)
- **Schedule**: GitHub Actions (daily cron, 02:00 UTC)
- **Hosting**: Vercel (auto-deployed after each pipeline run)

## Architecture

```
API Sources
    │
    ▼
Python extractors  →  DuckDB (raw schema)
                            │
                            ▼
                      dbt (staging → marts)
                            │
                            ▼
                   Evidence dashboard build
                            │
                            ▼
                    Vercel → jmhj.info
```

## Data Sources

| Source | Extractor | Raw tables | Mart tables |
|---|---|---|---|
| **Steam** | `steam.py` | `steam_owned_games`, `steam_profile`, `steam_achievements` | `steam_games` |
| **MyAnimeList** | `mal.py` | `mal_anime_list`, `mal_manga_list` | `mal_anime`, `mal_manga` |
| **Goodreads** | `goodreads.py` | `goodreads_books` | `goodreads_books` |
| **Spotify** | `spotify.py` | `spotify_top_tracks`, `spotify_top_artists`, `spotify_recently_played` | `spotify_top_tracks`, `spotify_top_artists`, `spotify_recently_played` |

## Dashboard Pages

| Page | Content |
|---|---|
| **Home** | Right Now snapshot + summary stats across all sources |
| **Steam → Games** | Full game library, playtime, achievement completion |
| **My Anime List → Anime** | Anime list with status breakdown and top rated |
| **My Anime List → Manga** | Manga list with status breakdown and top rated |
| **Goodreads → Books** | Books read by year, top rated, currently reading |
| **Spotify → Top Tracks** | Top 50 tracks by time range (4 weeks / 6 months / all time) |
| **Spotify → Top Artists** | Top 50 artists by time range |
| **Spotify → Recently Played** | Last 50 plays with hour-of-day and artist breakdowns |

## Project Structure

```
PersonalDataAggregationPipeline/
├── src/
│   └── extractors/          # One script per API source
│       ├── steam.py
│       ├── mal.py
│       ├── goodreads.py
│       └── spotify.py
├── scripts/
│   └── get_spotify_token.py # One-off OAuth helper for Spotify
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
│       └── pipeline.yml     # Daily cron + Vercel deploy
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
5. Copy `config/.env.example` to `.env` and fill in credentials
6. Run extractors: `python src/extractors/steam.py` (repeat for each source)
7. Run dbt: `cd dbt && dbt run --profiles-dir . && dbt test --profiles-dir .`

### Dashboard (local)

1. Install Node.js 18+ if needed
2. `cd dashboard && npm install`
3. `npm run sources` — pulls data from DuckDB into Evidence cache
4. `npm run dev` — starts dev server at `http://localhost:3000`

> Re-run `npm run sources` after each pipeline run to refresh local dashboard data.

### Spotify OAuth (one-time)

Spotify requires a refresh token obtained via OAuth. Run once:

```bash
venv\Scripts\python scripts\get_spotify_token.py
```

Follow the browser prompt, then copy the printed refresh token into `.env` as `SPOTIFY_REFRESH_TOKEN` and add it as a GitHub Actions secret.

## Environment Variables

See `config/.env.example` for all required variables. Sources and their required vars:

| Source | Variables |
|---|---|
| Steam | `STEAM_API_KEY`, `STEAM_ID` |
| MyAnimeList | `MAL_CLIENT_ID`, `MAL_USERNAME` |
| Goodreads | `GOODREADS_USER_ID` |
| Spotify | `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`, `SPOTIFY_REFRESH_TOKEN` |

## GitHub Actions

The pipeline runs daily at **02:00 UTC** and on manual trigger (`workflow_dispatch`).

Each run:
1. Runs all four extractors
2. Runs `dbt run` + `dbt test`
3. Uploads the DuckDB file as a workflow artifact (7-day retention)
4. Builds the Evidence dashboard
5. Deploys to Vercel → [jmhj.info](https://jmhj.info)

Required GitHub Actions secrets: `STEAM_API_KEY`, `STEAM_ID`, `MAL_CLIENT_ID`, `MAL_USERNAME`, `GOODREADS_USER_ID`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.
