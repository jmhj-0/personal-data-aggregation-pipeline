SELECT
    time_range,
    rank,
    track_id,
    track_name,
    artist_names,
    album_name,
    duration_secs,
    popularity,
    explicit,
    _loaded_at
FROM {{ ref('stg_spotify__top_tracks') }}
