import os
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_mal_data(client_id: str, username: str) -> List[Dict[str, Any]]:
    """
    Fetch MyAnimeList data for a user.

    Args:
        client_id: MAL API client ID
        username: MAL username

    Returns:
        List of anime data dictionaries
    """
    try:
        url = f"https://api.myanimelist.net/v2/users/{username}/animelist"
        headers = {'X-MAL-CLIENT-ID': client_id}
        params = {'limit': 1000}  # Adjust as needed

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        anime_list = response.json()['data']

        data = []
        for item in anime_list:
            try:
                anime = item['node']
                list_status = item.get('list_status', {})
                data.append({
                    'mal_id': anime['id'],
                    'title': anime['title'],
                    'status': list_status.get('status', 'unknown'),
                    'score': list_status.get('score', 0),
                    'episodes_watched': list_status.get('num_episodes_watched', 0),
                    'total_episodes': anime.get('num_episodes', 0),
                    'start_date': list_status.get('start_date'),
                    'end_date': list_status.get('finish_date'),
                    'fetched_at': datetime.now()
                })
            except KeyError as e:
                logger.warning(f"Skipping anime due to missing key: {e}")
                continue

        logger.info(f"Fetched {len(data)} anime from MAL for user {username}")
        return data
    except Exception as e:
        logger.error(f"Error fetching MAL data: {e}")
        return []

if __name__ == "__main__":
    # For testing
    client_id = os.getenv('MAL_CLIENT_ID')
    username = os.getenv('MAL_USERNAME')
    if client_id and username:
        data = get_mal_data(client_id, username)
        print(data[:5])  # Print first 5
    else:
        print("Set MAL_CLIENT_ID and MAL_USERNAME environment variables")