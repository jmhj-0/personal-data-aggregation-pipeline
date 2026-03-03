SELECT
    played_at,
    CAST(played_at AS DATE) AS play_date,
    EXTRACT(hour FROM played_at)::INTEGER AS play_hour,
    track_id,
    track_name,
    artist_names,
    album_name,
    duration_secs,
    _loaded_at
FROM {{ ref('stg_spotify__recently_played') }}
WHERE played_at IS NOT NULL
