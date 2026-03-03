# Personal Data Dashboard

```sql summary
select
    count(*) as total_games,
    round(sum(playtime_hours), 0) as total_playtime_hours,
    sum(total_achievements) as total_achievements,
    sum(achievements_unlocked) as total_unlocked
from personal_data.steam_games
```

```sql top_games
select
    game_name,
    playtime_hours,
    achievements_unlocked,
    total_achievements,
    achievement_completion_pct
from personal_data.steam_games
where playtime_hours > 0
order by playtime_hours desc
limit 20
```

```sql recently_played
select
    game_name,
    playtime_hours,
    last_played_at::date as last_played
from personal_data.steam_games
where last_played_at is not null
order by last_played_at desc
limit 10
```

## Steam

<BigValue data={summary} value="total_games" title="Games Owned" />
<BigValue data={summary} value="total_playtime_hours" title="Hours Played" />
<BigValue data={summary} value="total_unlocked" title="Achievements Unlocked" />

### Top 20 Games by Playtime

<BarChart
    data={top_games}
    x=game_name
    y=playtime_hours
    yAxisTitle="Hours"
    swapXY=true
/>

### Recently Played

<DataTable data={recently_played} />
