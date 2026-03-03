SELECT
    mal_id,
    title,
    media_type,
    airing_status,
    num_episodes,
    mean_score,
    genres,
    list_status,
    CASE WHEN list_score = 0 THEN NULL ELSE list_score END AS list_score,
    num_episodes_watched,
    is_rewatching,
    TRY_CAST(start_date AS DATE) AS started_at,
    TRY_CAST(finish_date AS DATE) AS finished_at,
    _loaded_at
FROM {{ source('raw', 'mal_anime_list') }}
