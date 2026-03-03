SELECT
    TRY_CAST(played_at AS TIMESTAMPTZ) AS played_at,
    track_id,
    track_name,
    artist_names,
    album_name,
    duration_ms,
    ROUND(duration_ms / 1000.0)::INTEGER AS duration_secs,
    _loaded_at
FROM {{ source('raw', 'spotify_recently_played') }}
