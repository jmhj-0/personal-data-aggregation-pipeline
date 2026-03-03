SELECT
    book_id,
    title,
    author,
    NULLIF(isbn, '') AS isbn,
    num_pages,
    avg_rating,
    CASE WHEN user_rating = 0 THEN NULL ELSE user_rating END AS user_rating,
    shelf,
    TRY_CAST(date_added AS DATE) AS date_added,
    TRY_CAST(date_read AS DATE) AS date_read,
    NULLIF(image_url, '') AS image_url,
    book_url,
    _loaded_at
FROM {{ source('raw', 'goodreads_books') }}
