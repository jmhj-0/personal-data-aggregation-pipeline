import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_spotify_data(client_id: str, client_secret: str, redirect_uri: str, username: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch recently played tracks from Spotify.

    Args:
        client_id: Spotify client ID
        client_secret: Spotify client secret
        redirect_uri: Redirect URI
        username: Spotify username
        limit: Number of tracks to fetch

    Returns:
        List of track data dictionaries
    """
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri,
                                                       scope="user-read-recently-played"))

        results = sp.current_user_recently_played(limit=limit)

        data = []
        for item in results['items']:
            track = item['track']
            data.append({
                'track_id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else '',
                'album': track['album']['name'],
                'played_at': item['played_at'],
                'duration_ms': track['duration_ms'],
                'fetched_at': datetime.now()
            })

        logger.info(f"Fetched {len(data)} tracks from Spotify for user {username}")
        return data
    except Exception as e:
        logger.error(f"Error fetching Spotify data: {e}")
        return []

if __name__ == "__main__":
    # For testing
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    username = os.getenv('SPOTIFY_USERNAME')
    if all([client_id, client_secret, redirect_uri, username]):
        data = get_spotify_data(client_id, client_secret, redirect_uri, username)
        print(data[:5])  # Print first 5
    else:
        print("Set Spotify environment variables")