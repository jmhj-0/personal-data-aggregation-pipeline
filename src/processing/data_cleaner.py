import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def clean_steam_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Clean Steam data."""
    df = pd.DataFrame(data)
    df['last_played'] = pd.to_datetime(df['last_played'], errors='coerce')
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    df = df.dropna(subset=['appid', 'name'])
    return df

def clean_mal_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Clean MAL data."""
    df = pd.DataFrame(data)
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    # Replace NaT with None for database compatibility
    df['start_date'] = df['start_date'].where(df['start_date'].notna(), None)
    df['end_date'] = df['end_date'].where(df['end_date'].notna(), None)
    df = df.dropna(subset=['mal_id', 'title'])
    return df

def clean_twitter_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Clean Twitter data."""
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    df = df.dropna(subset=['tweet_id', 'text'])
    return df

def clean_spotify_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Clean Spotify data."""
    df = pd.DataFrame(data)
    df['played_at'] = pd.to_datetime(df['played_at'])
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    df = df.dropna(subset=['track_id', 'name'])
    return df

def clean_github_data(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Clean GitHub data."""
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce')
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    df = df.dropna(subset=['repo_id', 'name'])
    return df

def process_data(source: str, data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Process and clean data based on source.

    Args:
        source: Data source ('steam', 'mal', 'twitter', 'spotify', 'github')
        data: Raw data list

    Returns:
        Cleaned DataFrame
    """
    cleaners = {
        'steam': clean_steam_data,
        'mal': clean_mal_data,
        'twitter': clean_twitter_data,
        'spotify': clean_spotify_data,
        'github': clean_github_data
    }

    if source in cleaners:
        df = cleaners[source](data)
        logger.info(f"Processed {len(df)} records from {source}")
        return df
    else:
        logger.error(f"Unknown source: {source}")
        return pd.DataFrame()