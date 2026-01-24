import logging
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ingestion.steam_ingest import get_steam_data
from ingestion.mal_ingest import get_mal_data
from ingestion.twitter_ingest import get_twitter_data
from ingestion.spotify_ingest import get_spotify_data
from ingestion.github_ingest import get_github_data
from processing.data_cleaner import process_data
from database.db_utils import create_tables, insert_data
from config.config import API_CONFIGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Run the full data aggregation pipeline."""
    logger.info("Starting data aggregation pipeline")

    # Create tables if not exist
    create_tables()

    # Define sources and their functions
    sources = {
        'steam': (get_steam_data, ['api_key', 'steam_id']),
        'mal': (get_mal_data, ['client_id', 'username']),
        'twitter': (get_twitter_data, ['bearer_token', 'username']),
        'spotify': (get_spotify_data, ['client_id', 'client_secret', 'redirect_uri', 'username']),
        'github': (get_github_data, ['token', 'username'])
    }

    # Table names
    table_names = {
        'steam': 'steam_games',
        'mal': 'mal_anime',
        'twitter': 'twitter_tweets',
        'spotify': 'spotify_tracks',
        'github': 'github_repos'
    }

    for source, (func, keys) in sources.items():
        config = API_CONFIGS.get(source, {})
        if not all(config.get(key) for key in keys):
            logger.warning(f"Skipping {source}: missing API credentials")
            continue

        try:
            # Fetch raw data
            if source == 'steam':
                data = func(config['api_key'], config['steam_id'])
            elif source == 'mal':
                data = func(config['client_id'], config['username'])
            elif source == 'twitter':
                data = func(config['bearer_token'], config['username'])
            elif source == 'spotify':
                data = func(config['client_id'], config['client_secret'], config['redirect_uri'], config['username'])
            elif source == 'github':
                data = func(config['token'], config['username'])

            if data:
                # Process data
                df = process_data(source, data)
                if not df.empty:
                    # Replace NaT with None for database compatibility
                    df = df.replace({pd.NaT: None})
                    # Insert into DB
                    insert_data(table_names[source], df.to_dict('records'))
                    logger.info(f"Successfully processed {len(df)} records for {source}")
                else:
                    logger.warning(f"No data to insert for {source}")
            else:
                logger.warning(f"No data fetched for {source}")
        except Exception as e:
            logger.error(f"Error processing {source}: {e}")

    logger.info("Data aggregation pipeline completed")

if __name__ == "__main__":
    run_pipeline()