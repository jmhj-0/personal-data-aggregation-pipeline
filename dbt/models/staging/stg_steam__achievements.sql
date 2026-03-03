SELECT
    appid,
    game_name,
    apiname AS achievement_key,
    achieved = 1 AS is_achieved,
    CASE
        WHEN unlocktime IS NULL OR unlocktime = 0 THEN NULL
        ELSE to_timestamp(unlocktime)
    END AS unlocked_at,
    _loaded_at
FROM {{ source('raw', 'steam_achievements') }}
