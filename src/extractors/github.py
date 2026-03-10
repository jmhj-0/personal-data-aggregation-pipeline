"""GitHub API extractor — loads profile and repo data into DuckDB."""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.github.com"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _gh_get(endpoint: str, token: str, params: dict | None = None) -> dict | list:
    response = requests.get(
        f"{_BASE_URL}/{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def load_profile(conn: duckdb.DuckDBPyConnection, token: str, username: str) -> int:
    """Fetch user profile and load into raw.github_profile."""
    data = _gh_get(f"users/{username}", token)
    loaded_at = datetime.now(timezone.utc)

    records = [(
        data.get("login", ""),
        data.get("name", ""),
        data.get("bio", ""),
        data.get("public_repos", 0),
        data.get("public_gists", 0),
        data.get("followers", 0),
        data.get("following", 0),
        data.get("created_at", ""),
        data.get("updated_at", ""),
        loaded_at,
    )]

    conn.execute("DROP TABLE IF EXISTS raw.github_profile")
    conn.execute("""
        CREATE TABLE raw.github_profile (
            login VARCHAR,
            name VARCHAR,
            bio VARCHAR,
            public_repos INTEGER,
            public_gists INTEGER,
            followers INTEGER,
            following INTEGER,
            created_at VARCHAR,
            updated_at VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.github_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", records)

    logger.info("Loaded profile for %s into raw.github_profile", username)
    return len(records)


def load_repos(conn: duckdb.DuckDBPyConnection, token: str, username: str) -> int:
    """Fetch owned repos (up to 100) and load into raw.github_repos."""
    data = _gh_get(
        f"users/{username}/repos",
        token,
        params={"type": "owner", "per_page": 100, "sort": "pushed"},
    )
    loaded_at = datetime.now(timezone.utc)

    records = [
        (
            repo["id"],
            repo.get("name", ""),
            repo.get("full_name", ""),
            repo.get("description", ""),
            repo.get("language", ""),
            repo.get("stargazers_count", 0),
            repo.get("forks_count", 0),
            repo.get("fork", False),
            repo.get("private", False),
            repo.get("created_at", ""),
            repo.get("pushed_at", ""),
            ", ".join(repo.get("topics", [])),
            loaded_at,
        )
        for repo in data
    ]

    conn.execute("DROP TABLE IF EXISTS raw.github_repos")
    conn.execute("""
        CREATE TABLE raw.github_repos (
            repo_id INTEGER,
            name VARCHAR,
            full_name VARCHAR,
            description VARCHAR,
            language VARCHAR,
            stargazers_count INTEGER,
            forks_count INTEGER,
            is_fork BOOLEAN,
            is_private BOOLEAN,
            created_at VARCHAR,
            pushed_at VARCHAR,
            topics VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany(
        "INSERT INTO raw.github_repos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        records,
    )

    logger.info("Loaded %d repos into raw.github_repos", len(records))
    return len(records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    token = os.environ["GH_PAT"]
    username = os.environ["GH_USERNAME"]

    conn = _get_conn()
    try:
        load_profile(conn, token, username)
        load_repos(conn, token, username)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
