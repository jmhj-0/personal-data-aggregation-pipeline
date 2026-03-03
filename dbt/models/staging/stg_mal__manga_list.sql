SELECT
    mal_id,
    title,
    media_type,
    num_volumes,
    num_chapters,
    mean_score,
    genres,
    list_status,
    CASE WHEN list_score = 0 THEN NULL ELSE list_score END AS list_score,
    num_volumes_read,
    num_chapters_read,
    is_rereading,
    TRY_CAST(start_date AS DATE) AS started_at,
    TRY_CAST(finish_date AS DATE) AS finished_at,
    _loaded_at
FROM {{ source('raw', 'mal_manga_list') }}
