SELECT
    mal_id,
    title,
    media_type,
    airing_status,
    num_episodes,
    mean_score,
    genres,
    list_status,
    list_score,
    num_episodes_watched,
    CASE
        WHEN num_episodes IS NULL OR num_episodes = 0 THEN NULL
        ELSE ROUND(num_episodes_watched * 1.0 / num_episodes, 3)
    END AS watch_progress_pct,
    is_rewatching,
    started_at,
    finished_at,
    _loaded_at
FROM {{ ref('stg_mal__anime_list') }}
