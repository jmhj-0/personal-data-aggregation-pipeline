SELECT
    time_range,
    rank,
    track_id,
    track_name,
    artist_names,
    album_name,
    duration_ms,
    ROUND(duration_ms / 1000.0)::INTEGER AS duration_secs,
    popularity,
    explicit,
    _loaded_at
FROM {{ source('raw', 'spotify_top_tracks') }}
