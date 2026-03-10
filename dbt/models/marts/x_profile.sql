SELECT
    user_id,
    name,
    username,
    description,
    followers_count,
    following_count,
    tweet_count,
    listed_count,
    created_at,
    _loaded_at
FROM {{ ref('stg_x__profile') }}
