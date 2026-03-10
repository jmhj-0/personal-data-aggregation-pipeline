SELECT
    user_id,
    name,
    username,
    description,
    followers_count,
    following_count,
    tweet_count,
    listed_count,
    created_at::TIMESTAMPTZ AS created_at,
    _loaded_at
FROM {{ source('raw', 'x_profile') }}
