SELECT
    tweet_id,
    text,
    created_at::TIMESTAMPTZ AS created_at,
    retweet_count,
    reply_count,
    like_count,
    quote_count,
    impression_count,
    _loaded_at
FROM {{ source('raw', 'x_tweets') }}
