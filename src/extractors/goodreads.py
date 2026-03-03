"""Goodreads RSS extractor — loads reading shelves into DuckDB.

Uses Goodreads public RSS feeds (no API key required).
Fetches three shelves: read, currently-reading, to-read.
"""

import logging
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree.ElementTree import fromstring

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_RSS_URL = "https://www.goodreads.com/review/list_rss/{user_id}?shelf={shelf}&per_page=200"
_SHELVES = ["read", "currently-reading", "to-read"]
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _parse_date(value: str | None) -> str | None:
    """Parse an RFC 822 date string to an ISO date string, or return None."""
    if not value or not value.strip():
        return None
    try:
        return parsedate_to_datetime(value).date().isoformat()
    except Exception:
        return None


def _fetch_shelf(user_id: str, shelf: str) -> list[dict]:
    url = _RSS_URL.format(user_id=user_id, shelf=shelf)
    response = requests.get(url, timeout=15, headers={"User-Agent": "personal-data-pipeline/1.0"})
    response.raise_for_status()

    root = fromstring(response.content)
    items = root.findall(".//item")

    records = []
    for item in items:
        num_pages_text = item.findtext("num_pages")
        avg_rating_text = item.findtext("average_rating")
        user_rating_text = item.findtext("user_rating")

        records.append({
            "book_id": item.findtext("book_id", ""),
            "title": item.findtext("title", ""),
            "author": item.findtext("author_name", ""),
            "isbn": item.findtext("isbn", ""),
            "num_pages": int(num_pages_text) if num_pages_text and num_pages_text.strip().isdigit() else None,
            "avg_rating": float(avg_rating_text) if avg_rating_text and avg_rating_text.strip() else None,
            "user_rating": int(user_rating_text) if user_rating_text and user_rating_text.strip().isdigit() else None,
            "shelf": shelf,
            "date_added": _parse_date(item.findtext("user_date_added")),
            "date_read": _parse_date(item.findtext("user_read_at")),
            "image_url": item.findtext("book_large_image_url", ""),
            "book_url": item.findtext("link", ""),
        })

    logger.info("Fetched %d books from '%s' shelf", len(records), shelf)
    return records


def load_books(conn: duckdb.DuckDBPyConnection, user_id: str) -> int:
    """Fetch all reading shelves and load into raw.goodreads_books."""
    loaded_at = datetime.now(timezone.utc)
    all_records = []

    for shelf in _SHELVES:
        all_records.extend(_fetch_shelf(user_id, shelf))

    records = [
        (
            r["book_id"],
            r["title"],
            r["author"],
            r["isbn"],
            r["num_pages"],
            r["avg_rating"],
            r["user_rating"],
            r["shelf"],
            r["date_added"],
            r["date_read"],
            r["image_url"],
            r["book_url"],
            loaded_at,
        )
        for r in all_records
    ]

    conn.execute("DROP TABLE IF EXISTS raw.goodreads_books")
    conn.execute("""
        CREATE TABLE raw.goodreads_books (
            book_id VARCHAR,
            title VARCHAR,
            author VARCHAR,
            isbn VARCHAR,
            num_pages INTEGER,
            avg_rating DOUBLE,
            user_rating INTEGER,
            shelf VARCHAR,
            date_added VARCHAR,
            date_read VARCHAR,
            image_url VARCHAR,
            book_url VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany(
        "INSERT INTO raw.goodreads_books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        records,
    )

    logger.info("Loaded %d total books into raw.goodreads_books", len(records))
    return len(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    user_id = os.environ["GOODREADS_USER_ID"]

    conn = _get_conn()
    try:
        load_books(conn, user_id)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
