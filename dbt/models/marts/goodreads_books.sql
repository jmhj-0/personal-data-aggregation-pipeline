SELECT
    book_id,
    title,
    author,
    isbn,
    num_pages,
    avg_rating,
    user_rating,
    shelf,
    date_added,
    date_read,
    EXTRACT(year FROM date_read) AS year_read,
    image_url,
    book_url,
    _loaded_at
FROM {{ ref('stg_goodreads__books') }}
