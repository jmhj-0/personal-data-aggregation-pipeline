"""Spotify API extractor — loads top tracks, top artists, and recently played into DuckDB."""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.spotify.com/v1"
_TOKEN_URL = "https://accounts.spotify.com/api/token"
_TIME_RANGES = ["short_term", "medium_term", "long_term"]
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _get_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    response = requests.post(
        _TOKEN_URL,
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        auth=(client_id, client_secret),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _spotify_get(endpoint: str, access_token: str, params: dict | None = None) -> dict:
    response = requests.get(
        f"{_BASE_URL}/{endpoint}",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def load_top_tracks(conn: duckdb.DuckDBPyConnection, access_token: str) -> int:
    """Fetch top 50 tracks per time range and load into raw.spotify_top_tracks."""
    loaded_at = datetime.now(timezone.utc)
    records = []

    for time_range in _TIME_RANGES:
        data = _spotify_get("me/top/tracks", access_token, {"limit": 50, "time_range": time_range})
        for rank, item in enumerate(data.get("items", []), start=1):
            records.append((
                time_range,
                rank,
                item["id"],
                item["name"],
                ", ".join(a["name"] for a in item.get("artists", [])),
                item.get("album", {}).get("name", ""),
                item.get("duration_ms"),
                item.get("popularity"),
                item.get("explicit", False),
                loaded_at,
            ))
        logger.info("Fetched %d top tracks for %s", len(data.get("items", [])), time_range)

    conn.execute("DROP TABLE IF EXISTS raw.spotify_top_tracks")
    conn.execute("""
        CREATE TABLE raw.spotify_top_tracks (
            time_range VARCHAR,
            rank INTEGER,
            track_id VARCHAR,
            track_name VARCHAR,
            artist_names VARCHAR,
            album_name VARCHAR,
            duration_ms INTEGER,
            popularity INTEGER,
            explicit BOOLEAN,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.spotify_top_tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", records)
    logger.info("Loaded %d rows into raw.spotify_top_tracks", len(records))
    return len(records)


def load_top_artists(conn: duckdb.DuckDBPyConnection, access_token: str) -> int:
    """Fetch top 50 artists per time range and load into raw.spotify_top_artists."""
    loaded_at = datetime.now(timezone.utc)
    records = []

    for time_range in _TIME_RANGES:
        data = _spotify_get("me/top/artists", access_token, {"limit": 50, "time_range": time_range})
        for rank, item in enumerate(data.get("items", []), start=1):
            records.append((
                time_range,
                rank,
                item["id"],
                item["name"],
                ", ".join(item.get("genres", [])),
                item.get("popularity"),
                item.get("followers", {}).get("total"),
                loaded_at,
            ))
        logger.info("Fetched %d top artists for %s", len(data.get("items", [])), time_range)

    conn.execute("DROP TABLE IF EXISTS raw.spotify_top_artists")
    conn.execute("""
        CREATE TABLE raw.spotify_top_artists (
            time_range VARCHAR,
            rank INTEGER,
            artist_id VARCHAR,
            artist_name VARCHAR,
            genres VARCHAR,
            popularity INTEGER,
            followers INTEGER,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.spotify_top_artists VALUES (?, ?, ?, ?, ?, ?, ?, ?)", records)
    logger.info("Loaded %d rows into raw.spotify_top_artists", len(records))
    return len(records)


def load_recently_played(conn: duckdb.DuckDBPyConnection, access_token: str) -> int:
    """Fetch last 50 played tracks and load into raw.spotify_recently_played."""
    loaded_at = datetime.now(timezone.utc)
    data = _spotify_get("me/player/recently-played", access_token, {"limit": 50})

    records = [
        (
            item.get("played_at", ""),
            item.get("track", {}).get("id", ""),
            item.get("track", {}).get("name", ""),
            ", ".join(a["name"] for a in item.get("track", {}).get("artists", [])),
            item.get("track", {}).get("album", {}).get("name", ""),
            item.get("track", {}).get("duration_ms"),
            loaded_at,
        )
        for item in data.get("items", [])
    ]

    conn.execute("DROP TABLE IF EXISTS raw.spotify_recently_played")
    conn.execute("""
        CREATE TABLE raw.spotify_recently_played (
            played_at VARCHAR,
            track_id VARCHAR,
            track_name VARCHAR,
            artist_names VARCHAR,
            album_name VARCHAR,
            duration_ms INTEGER,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.spotify_recently_played VALUES (?, ?, ?, ?, ?, ?, ?)", records)
    logger.info("Loaded %d rows into raw.spotify_recently_played", len(records))
    return len(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    refresh_token = os.environ["SPOTIFY_REFRESH_TOKEN"]

    access_token = _get_access_token(client_id, client_secret, refresh_token)
    logger.info("Access token obtained")

    conn = _get_conn()
    try:
        load_top_tracks(conn, access_token)
        load_top_artists(conn, access_token)
        load_recently_played(conn, access_token)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
