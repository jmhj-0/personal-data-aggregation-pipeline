"""Steam API extractor — loads raw Steam data into DuckDB."""

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.steampowered.com"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DB_PATH = _PROJECT_ROOT / "data" / "personal_data.duckdb"


def _get_conn() -> duckdb.DuckDBPyConnection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(_DB_PATH))
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    return conn


def _steam_get(endpoint: str, params: dict) -> dict:
    url = f"{_BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def load_owned_games(conn: duckdb.DuckDBPyConnection, api_key: str, steam_id: str) -> int:
    """Fetch owned games and load into raw.steam_owned_games."""
    data = _steam_get(
        "IPlayerService/GetOwnedGames/v1/",
        params={
            "key": api_key,
            "steamid": steam_id,
            "include_appinfo": 1,
            "include_played_free_games": 1,
        },
    )

    games = data.get("response", {}).get("games", [])
    loaded_at = datetime.now(timezone.utc)

    records = [
        (
            game["appid"],
            game.get("name", ""),
            game.get("playtime_forever", 0),
            game.get("playtime_2weeks"),
            game.get("rtime_last_played"),
            loaded_at,
        )
        for game in games
    ]

    conn.execute("DROP TABLE IF EXISTS raw.steam_owned_games")
    conn.execute("""
        CREATE TABLE raw.steam_owned_games (
            appid INTEGER,
            name VARCHAR,
            playtime_forever INTEGER,
            playtime_2weeks INTEGER,
            rtime_last_played BIGINT,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.steam_owned_games VALUES (?, ?, ?, ?, ?, ?)", records)

    logger.info("Loaded %d games into raw.steam_owned_games", len(records))
    return len(records)


def load_player_summary(conn: duckdb.DuckDBPyConnection, api_key: str, steam_id: str) -> int:
    """Fetch player profile and load into raw.steam_profile."""
    data = _steam_get(
        "ISteamUser/GetPlayerSummaries/v2/",
        params={
            "key": api_key,
            "steamids": steam_id,
        },
    )

    players = data.get("response", {}).get("players", [])
    loaded_at = datetime.now(timezone.utc)

    records = [
        (
            p.get("steamid", ""),
            p.get("personaname", ""),
            p.get("profileurl", ""),
            p.get("avatar", ""),
            p.get("personastate"),
            p.get("communityvisibilitystate"),
            p.get("timecreated"),
            p.get("loccountrycode"),
            loaded_at,
        )
        for p in players
    ]

    conn.execute("DROP TABLE IF EXISTS raw.steam_profile")
    conn.execute("""
        CREATE TABLE raw.steam_profile (
            steamid VARCHAR,
            personaname VARCHAR,
            profileurl VARCHAR,
            avatar VARCHAR,
            personastate INTEGER,
            communityvisibilitystate INTEGER,
            timecreated BIGINT,
            loccountrycode VARCHAR,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.steam_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", records)

    logger.info("Loaded %d profile(s) into raw.steam_profile", len(records))
    return len(records)


def load_achievements(conn: duckdb.DuckDBPyConnection, api_key: str, steam_id: str) -> int:
    """Fetch achievements for played games and load into raw.steam_achievements.

    Only queries games with playtime > 0 to avoid excessive API calls.
    Games with no achievement data (e.g. no stats schema) are skipped silently.
    """
    data = _steam_get(
        "IPlayerService/GetOwnedGames/v1/",
        params={
            "key": api_key,
            "steamid": steam_id,
            "include_appinfo": 1,
            "include_played_free_games": 1,
        },
    )
    played_games = [
        g for g in data.get("response", {}).get("games", [])
        if g.get("playtime_forever", 0) > 0
    ]

    loaded_at = datetime.now(timezone.utc)
    all_records = []

    for i, game in enumerate(played_games, start=1):
        appid = game["appid"]
        game_name = game.get("name", "")
        logger.debug("Fetching achievements for %s (%d/%d)", game_name, i, len(played_games))

        try:
            ach_data = _steam_get(
                "ISteamUserStats/GetPlayerAchievements/v1/",
                params={
                    "key": api_key,
                    "steamid": steam_id,
                    "appid": appid,
                    "l": "english",
                },
            )
            achievements = ach_data.get("playerstats", {}).get("achievements", [])
            for ach in achievements:
                all_records.append((
                    appid,
                    game_name,
                    ach.get("apiname", ""),
                    ach.get("achieved", 0),
                    ach.get("unlocktime", 0),
                    loaded_at,
                ))
        except requests.HTTPError:
            logger.debug("No achievement data for %s (appid %d) — skipping", game_name, appid)

    conn.execute("DROP TABLE IF EXISTS raw.steam_achievements")
    conn.execute("""
        CREATE TABLE raw.steam_achievements (
            appid INTEGER,
            game_name VARCHAR,
            apiname VARCHAR,
            achieved INTEGER,
            unlocktime BIGINT,
            _loaded_at TIMESTAMPTZ
        )
    """)
    conn.executemany("INSERT INTO raw.steam_achievements VALUES (?, ?, ?, ?, ?, ?)", all_records)

    logger.info(
        "Loaded %d achievements across %d played games into raw.steam_achievements",
        len(all_records),
        len(played_games),
    )
    return len(all_records)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )

    load_dotenv(_PROJECT_ROOT / ".env")

    api_key = os.environ["STEAM_API_KEY"]
    steam_id = os.environ["STEAM_ID"]

    conn = _get_conn()
    try:
        load_owned_games(conn, api_key, steam_id)
        load_player_summary(conn, api_key, steam_id)
        load_achievements(conn, api_key, steam_id)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
