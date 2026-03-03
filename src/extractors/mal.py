"""MyAnimeList API extractor — loads raw MAL data into DuckDB."""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.myanimelist.net/v2"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"

_ANIME_FIELDS = (
    "list_status{status,score,num_episodes_watched,is_rewatching,start_date,finish_date},"
    "num_episodes,mean,media_type,status,genres"
)
_MANGA_FIELDS = (
    "list_status{status,score,num_volumes_read,num_chapters_read,is_rereading,start_date,finish_date},"
    "num_volumes,num_chapters,mean,media_type,genres"
)


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _mal_paginate(endpoint: str, client_id: str, params: dict) -> Generator[dict, None, None]:
    """Yield every item from a paginated MAL v2 endpoint."""
    headers = {"X-MAL-CLIENT-ID": client_id}
    url = f"{_BASE_URL}/{endpoint}"

    while url:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        body = response.json()

        for item in body.get("data", []):
            yield item

        url = body.get("paging", {}).get("next")
        params = {}  # next URL already encodes all params


def load_anime_list(conn: duckdb.DuckDBPyConnection, client_id: str, username: str) -> int:
    """Fetch user anime list and load into raw.mal_anime_list."""
    loaded_at = datetime.now(timezone.utc)
    records = []

    for item in _mal_paginate(
        f"users/{username}/animelist",
        client_id,
        params={"fields": _ANIME_FIELDS, "limit": 1000, "nsfw": "true"},
    ):
        node = item.get("node", {})
        status = item.get("list_status", {})
        genres = ",".join(g["name"] for g in node.get("genres", []))

        records.append((
            node.get("id"),
            node.get("title", ""),
            node.get("media_type", ""),
            node.get("status", ""),
            node.get("num_episodes"),
            node.get("mean"),
            genres,
            status.get("status", ""),
            status.get("score", 0),
            status.get("num_episodes_watched", 0),
            status.get("is_rewatching", False),
            status.get("start_date"),
            status.get("finish_date"),
            loaded_at,
        ))

    conn.execute("DROP TABLE IF EXISTS raw.mal_anime_list")
    conn.execute("""
        CREATE TABLE raw.mal_anime_list (
            mal_id INTEGER,
            title VARCHAR,
            media_type VARCHAR,
            airing_status VARCHAR,
            num_episodes INTEGER,
            mean_score DOUBLE,
            genres VARCHAR,
            list_status VARCHAR,
            list_score INTEGER,
            num_episodes_watched INTEGER,
            is_rewatching BOOLEAN,
            start_date VARCHAR,
            finish_date VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany(
        "INSERT INTO raw.mal_anime_list VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        records,
    )

    logger.info("Loaded %d anime entries into raw.mal_anime_list", len(records))
    return len(records)


def load_manga_list(conn: duckdb.DuckDBPyConnection, client_id: str, username: str) -> int:
    """Fetch user manga list and load into raw.mal_manga_list."""
    loaded_at = datetime.now(timezone.utc)
    records = []

    for item in _mal_paginate(
        f"users/{username}/mangalist",
        client_id,
        params={"fields": _MANGA_FIELDS, "limit": 1000, "nsfw": "true"},
    ):
        node = item.get("node", {})
        status = item.get("list_status", {})
        genres = ",".join(g["name"] for g in node.get("genres", []))

        records.append((
            node.get("id"),
            node.get("title", ""),
            node.get("media_type", ""),
            node.get("num_volumes"),
            node.get("num_chapters"),
            node.get("mean"),
            genres,
            status.get("status", ""),
            status.get("score", 0),
            status.get("num_volumes_read", 0),
            status.get("num_chapters_read", 0),
            status.get("is_rereading", False),
            status.get("start_date"),
            status.get("finish_date"),
            loaded_at,
        ))

    conn.execute("DROP TABLE IF EXISTS raw.mal_manga_list")
    conn.execute("""
        CREATE TABLE raw.mal_manga_list (
            mal_id INTEGER,
            title VARCHAR,
            media_type VARCHAR,
            num_volumes INTEGER,
            num_chapters INTEGER,
            mean_score DOUBLE,
            genres VARCHAR,
            list_status VARCHAR,
            list_score INTEGER,
            num_volumes_read INTEGER,
            num_chapters_read INTEGER,
            is_rereading BOOLEAN,
            start_date VARCHAR,
            finish_date VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany(
        "INSERT INTO raw.mal_manga_list VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        records,
    )

    logger.info("Loaded %d manga entries into raw.mal_manga_list", len(records))
    return len(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    client_id = os.environ["MAL_CLIENT_ID"]
    username = os.environ["MAL_USERNAME"]

    conn = _get_conn()
    try:
        load_anime_list(conn, client_id, username)
        load_manga_list(conn, client_id, username)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
