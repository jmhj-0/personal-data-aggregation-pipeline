# Personal Data Aggregation Pipeline

This project aggregates personal data from various online services (Steam, MyAnimeList, X/Twitter, Spotify, GitHub) into a PostgreSQL database for analysis and visualization with Metabase.

## Setup

1. Clone or download the project.
2. Create a virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up PostgreSQL database (local or Docker).
6. Copy `config/.env.example` to `.env` and fill in your API keys and DB credentials.
7. Run the pipeline: `python src/main.py`
8. For scheduling: `python src/scheduler.py` (runs daily at 2 AM)
9. Set up Metabase to connect to the PostgreSQL DB and create dashboards.

## APIs Required

- Steam: API key and Steam ID
- MyAnimeList: Client ID and username
- Twitter: API keys and access tokens
- Spotify: Client ID/Secret and username
- GitHub: Personal access token

## Database Schema

See `src/database/schema.sql` for table definitions.

## Testing

Run tests: `python -m unittest tests/test_pipeline.py`

## Notes

- Ensure all API credentials are set in environment variables.
- PostgreSQL must be running and accessible.
- For Metabase, use Docker: `docker run -d -p 3000:3000 --name metabase metabase/metabase`