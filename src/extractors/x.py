"""X (Twitter) API v2 extractor — loads profile and tweets into DuckDB.

Uses app-only OAuth 2.0 Bearer Token.
Requires Basic tier or above on the X Developer Platform to read tweets.
"""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.twitter.com/2"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _x_get(endpoint: str, bearer_token: str, params: dict | None = None) -> dict:
    response = requests.get(
        f"{_BASE_URL}/{endpoint}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def _get_user_id(bearer_token: str, username: str) -> str:
    data = _x_get(
        f"users/by/username/{username}",
        bearer_token,
        params={"user.fields": "public_metrics,created_at,description"},
    )
    return data["data"]["id"]


def load_profile(conn: duckdb.DuckDBPyConnection, bearer_token: str, username: str) -> str:
    """Fetch user profile and load into raw.x_profile. Returns the user ID."""
    data = _x_get(
        f"users/by/username/{username}",
        bearer_token,
        params={"user.fields": "public_metrics,created_at,description"},
    )
    loaded_at = datetime.now(timezone.utc)
    user = data["data"]
    metrics = user.get("public_metrics", {})

    records = [(
        user["id"],
        user.get("name", ""),
        user.get("username", ""),
        user.get("description", ""),
        metrics.get("followers_count", 0),
        metrics.get("following_count", 0),
        metrics.get("tweet_count", 0),
        metrics.get("listed_count", 0),
        user.get("created_at", ""),
        loaded_at,
    )]

    conn.execute("DROP TABLE IF EXISTS raw.x_profile")
    conn.execute("""
        CREATE TABLE raw.x_profile (
            user_id VARCHAR,
            name VARCHAR,
            username VARCHAR,
            description VARCHAR,
            followers_count INTEGER,
            following_count INTEGER,
            tweet_count INTEGER,
            listed_count INTEGER,
            created_at VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.x_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", records)

    logger.info("Loaded profile for @%s into raw.x_profile", username)
    return user["id"]


def load_tweets(conn: duckdb.DuckDBPyConnection, bearer_token: str, user_id: str) -> int:
    """Fetch up to 100 recent tweets and load into raw.x_tweets."""
    data = _x_get(
        f"users/{user_id}/tweets",
        bearer_token,
        params={
            "max_results": 100,
            "tweet.fields": "created_at,public_metrics",
            "exclude": "retweets,replies",
        },
    )
    loaded_at = datetime.now(timezone.utc)
    tweets = data.get("data", [])

    records = [
        (
            tweet["id"],
            tweet.get("text", ""),
            tweet.get("created_at", ""),
            tweet.get("public_metrics", {}).get("retweet_count", 0),
            tweet.get("public_metrics", {}).get("reply_count", 0),
            tweet.get("public_metrics", {}).get("like_count", 0),
            tweet.get("public_metrics", {}).get("quote_count", 0),
            tweet.get("public_metrics", {}).get("impression_count"),
            loaded_at,
        )
        for tweet in tweets
    ]

    conn.execute("DROP TABLE IF EXISTS raw.x_tweets")
    conn.execute("""
        CREATE TABLE raw.x_tweets (
            tweet_id VARCHAR,
            text VARCHAR,
            created_at VARCHAR,
            retweet_count INTEGER,
            reply_count INTEGER,
            like_count INTEGER,
            quote_count INTEGER,
            impression_count INTEGER,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.x_tweets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", records)

    logger.info("Loaded %d tweets into raw.x_tweets", len(records))
    return len(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    bearer_token = os.environ["X_BEARER_TOKEN"]
    username = os.environ["X_USERNAME"]

    conn = _get_conn()
    try:
        user_id = load_profile(conn, bearer_token, username)
        load_tweets(conn, bearer_token, user_id)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
