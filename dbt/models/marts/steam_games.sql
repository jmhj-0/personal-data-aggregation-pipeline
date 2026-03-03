WITH games AS (
    SELECT * FROM {{ ref('stg_steam__owned_games') }}
),

achievement_stats AS (
    SELECT
        appid,
        COUNT(*) AS total_achievements,
        SUM(CASE WHEN is_achieved THEN 1 ELSE 0 END) AS achievements_unlocked
    FROM {{ ref('stg_steam__achievements') }}
    GROUP BY appid
)

SELECT
    g.appid,
    g.game_name,
    g.playtime_minutes,
    ROUND(g.playtime_minutes / 60.0, 1) AS playtime_hours,
    g.playtime_2weeks_minutes,
    ROUND(g.playtime_2weeks_minutes / 60.0, 1) AS playtime_2weeks_hours,
    g.last_played_at,
    COALESCE(a.total_achievements, 0) AS total_achievements,
    COALESCE(a.achievements_unlocked, 0) AS achievements_unlocked,
    CASE
        WHEN COALESCE(a.total_achievements, 0) = 0 THEN NULL
        ELSE ROUND(a.achievements_unlocked * 1.0 / a.total_achievements, 3)
    END AS achievement_completion_pct,
    g._loaded_at
FROM games g
LEFT JOIN achievement_stats a ON g.appid = a.appid
