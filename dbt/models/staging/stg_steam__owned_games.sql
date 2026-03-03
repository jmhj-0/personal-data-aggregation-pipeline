SELECT
    appid,
    name AS game_name,
    playtime_forever AS playtime_minutes,
    COALESCE(playtime_2weeks, 0) AS playtime_2weeks_minutes,
    CASE
        WHEN rtime_last_played IS NULL OR rtime_last_played = 0 THEN NULL
        ELSE to_timestamp(rtime_last_played)
    END AS last_played_at,
    _loaded_at
FROM {{ source('raw', 'steam_owned_games') }}
