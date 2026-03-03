SELECT
    mal_id,
    title,
    media_type,
    num_volumes,
    num_chapters,
    mean_score,
    genres,
    list_status,
    list_score,
    num_volumes_read,
    num_chapters_read,
    CASE
        WHEN num_chapters IS NULL OR num_chapters = 0 THEN NULL
        ELSE ROUND(num_chapters_read * 1.0 / num_chapters, 3)
    END AS read_progress_pct,
    is_rereading,
    started_at,
    finished_at,
    _loaded_at
FROM {{ ref('stg_mal__manga_list') }}
