SELECT
    steamid,
    personaname AS display_name,
    profileurl AS profile_url,
    avatar AS avatar_url,
    CASE personastate
        WHEN 0 THEN 'Offline'
        WHEN 1 THEN 'Online'
        WHEN 2 THEN 'Busy'
        WHEN 3 THEN 'Away'
        WHEN 4 THEN 'Snooze'
        WHEN 5 THEN 'Looking to trade'
        WHEN 6 THEN 'Looking to play'
        ELSE 'Unknown'
    END AS persona_state,
    communityvisibilitystate,
    CASE
        WHEN timecreated IS NULL THEN NULL
        ELSE to_timestamp(timecreated)
    END AS account_created_at,
    loccountrycode AS country_code,
    _loaded_at
FROM {{ source('raw', 'steam_profile') }}
