import os
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_twitter_data(bearer_token: str, username: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch recent tweets for a user using Twitter API v2.

    Args:
        bearer_token: Twitter Bearer Token
        username: Twitter username
        count: Number of tweets to fetch

    Returns:
        List of tweet data dictionaries
    """
    try:
        headers = {'Authorization': f'Bearer {bearer_token}'}

        # Get user ID
        user_url = f"https://api.twitter.com/2/users/by/username/{username}"
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_id = user_response.json()['data']['id']

        # Get tweets
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {'max_results': min(count, 100), 'tweet.fields': 'created_at,public_metrics'}
        tweets_response = requests.get(tweets_url, headers=headers, params=params)
        tweets_response.raise_for_status()
        tweets_data = tweets_response.json()['data']

        data = []
        for tweet in tweets_data:
            metrics = tweet['public_metrics']
            data.append({
                'tweet_id': tweet['id'],
                'text': tweet['text'],
                'created_at': tweet['created_at'],
                'retweets': metrics['retweet_count'],
                'likes': metrics['like_count'],
                'replies': metrics['reply_count'],
                'fetched_at': datetime.now()
            })

        logger.info(f"Fetched {len(data)} tweets from Twitter for user {username}")
        return data
    except Exception as e:
        logger.error(f"Error fetching Twitter data: {e}")
        return []

if __name__ == "__main__":
    # For testing
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    username = os.getenv('TWITTER_USERNAME')
    if bearer_token and username:
        data = get_twitter_data(bearer_token, username)
        print(data[:5])  # Print first 5
    else:
        print("Set TWITTER_BEARER_TOKEN and TWITTER_USERNAME environment variables")