SELECT
    time_range,
    rank,
    artist_id,
    artist_name,
    genres,
    popularity,
    followers,
    _loaded_at
FROM {{ source('raw', 'spotify_top_artists') }}
