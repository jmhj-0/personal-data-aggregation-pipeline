-- Database schema for Personal Data Aggregation Pipeline
-- PostgreSQL

-- Steam data
CREATE TABLE IF NOT EXISTS steam_games (
    id SERIAL PRIMARY KEY,
    appid INTEGER UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    playtime_forever INTEGER,
    playtime_2weeks INTEGER,
    last_played TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MyAnimeList data
CREATE TABLE IF NOT EXISTS mal_anime (
    id SERIAL PRIMARY KEY,
    mal_id INTEGER UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    status VARCHAR(50),
    score DECIMAL(3,2),
    episodes_watched INTEGER,
    total_episodes INTEGER,
    start_date DATE,
    end_date DATE,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- X/Twitter data
CREATE TABLE IF NOT EXISTS twitter_tweets (
    id SERIAL PRIMARY KEY,
    tweet_id BIGINT UNIQUE NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    retweets INTEGER,
    likes INTEGER,
    replies INTEGER,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spotify data
CREATE TABLE IF NOT EXISTS spotify_tracks (
    id SERIAL PRIMARY KEY,
    track_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255),
    album VARCHAR(255),
    played_at TIMESTAMP NOT NULL,
    duration_ms INTEGER,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GitHub data
CREATE TABLE IF NOT EXISTS github_repos (
    id SERIAL PRIMARY KEY,
    repo_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    description TEXT,
    language VARCHAR(100),
    stars INTEGER,
    forks INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_steam_appid ON steam_games(appid);
CREATE INDEX IF NOT EXISTS idx_mal_mal_id ON mal_anime(mal_id);
CREATE INDEX IF NOT EXISTS idx_twitter_tweet_id ON twitter_tweets(tweet_id);
CREATE INDEX IF NOT EXISTS idx_spotify_track_id ON spotify_tracks(track_id);
CREATE INDEX IF NOT EXISTS idx_github_repo_id ON github_repos(repo_id);