SELECT
    tweet_id,
    text,
    created_at,
    retweet_count,
    reply_count,
    like_count,
    quote_count,
    impression_count,
    retweet_count + reply_count + like_count + quote_count AS total_engagements,
    _loaded_at
FROM {{ ref('stg_x__tweets') }}
