import os
import logging
from steam.webapi import WebAPI
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_steam_data(api_key: str, steam_id: str) -> List[Dict[str, Any]]:
    """
    Fetch Steam game data for a user.

    Args:
        api_key: Steam API key
        steam_id: User's Steam ID

    Returns:
        List of game data dictionaries
    """
    try:
        steam = WebAPI(api_key)
        games = steam.call('IPlayerService.GetOwnedGames', steamid=steam_id, appids_filter=[], include_appinfo=1, include_played_free_games=1, include_free_sub=1, language='english')

        data = []
        for game in games['response']['games']:
            data.append({
                'appid': game['appid'],
                'name': game['name'],
                'playtime_forever': game.get('playtime_forever', 0),
                'playtime_2weeks': game.get('playtime_2weeks', 0),
                'last_played': datetime.fromtimestamp(game.get('rtime_last_played', 0)) if game.get('rtime_last_played') else None,
                'fetched_at': datetime.now()
            })

        logger.info(f"Fetched {len(data)} games from Steam for user {steam_id}")
        return data
    except Exception as e:
        logger.error(f"Error fetching Steam data: {e}")
        return []

if __name__ == "__main__":
    # For testing
    api_key = os.getenv('STEAM_API_KEY')
    steam_id = os.getenv('STEAM_ID')
    if api_key and steam_id:
        data = get_steam_data(api_key, steam_id)
        print(data[:5])  # Print first 5
    else:
        print("Set STEAM_API_KEY and STEAM_ID environment variables")