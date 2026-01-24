import os

# Database config
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'name': os.getenv('DB_NAME', 'personal_data'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# API configs
API_CONFIGS = {
    'steam': {
        'api_key': os.getenv('STEAM_API_KEY'),
        'steam_id': os.getenv('STEAM_ID')
    },
    'mal': {
        'client_id': os.getenv('MAL_CLIENT_ID'),
        'username': os.getenv('MAL_USERNAME')
    },
    'twitter': {
        'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
        'username': os.getenv('TWITTER_USERNAME')
    },
    'spotify': {
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
        'redirect_uri': os.getenv('SPOTIFY_REDIRECT_URI'),
        'username': os.getenv('SPOTIFY_USERNAME')
    },
    'github': {
        'token': os.getenv('GITHUB_TOKEN'),
        'username': os.getenv('GITHUB_USERNAME')
    }
}