SELECT
    time_range,
    rank,
    artist_id,
    artist_name,
    genres,
    popularity,
    followers,
    _loaded_at
FROM {{ ref('stg_spotify__top_artists') }}
