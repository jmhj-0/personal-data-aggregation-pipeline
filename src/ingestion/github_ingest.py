import os
import logging
from github import Github
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_github_data(token: str, username: str) -> List[Dict[str, Any]]:
    """
    Fetch GitHub repositories for a user.

    Args:
        token: GitHub personal access token
        username: GitHub username

    Returns:
        List of repository data dictionaries
    """
    try:
        g = Github(token)
        user = g.get_user(username)
        repos = user.get_repos()

        data = []
        for repo in repos:
            data.append({
                'repo_id': repo.id,
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'fetched_at': datetime.now()
            })

        logger.info(f"Fetched {len(data)} repos from GitHub for user {username}")
        return data
    except Exception as e:
        logger.error(f"Error fetching GitHub data: {e}")
        return []

if __name__ == "__main__":
    # For testing
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')
    if token and username:
        data = get_github_data(token, username)
        print(data[:5])  # Print first 5
    else:
        print("Set GITHUB_TOKEN and GITHUB_USERNAME environment variables")