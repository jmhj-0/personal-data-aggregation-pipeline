# Steam — All Games

```sql games
select
    game_name,
    playtime_hours,
    last_played_at::date as last_played,
    total_achievements,
    achievements_unlocked,
    achievement_completion_pct
from personal_data.steam_games
order by playtime_hours desc
```

```sql completion_buckets
select
    case
        when achievement_completion_pct is null then 'No achievements'
        when achievement_completion_pct = 100 then '100% complete'
        when achievement_completion_pct >= 50 then '50–99%'
        when achievement_completion_pct >= 1 then '1–49%'
        else '0%'
    end as bucket,
    count(*) as games
from personal_data.steam_games
group by bucket
order by games desc
```

<BigValue data={games} value="playtime_hours" title="Total Hours" fmt="num0" />

### Achievement Completion Breakdown

<BarChart
    data={completion_buckets}
    x=bucket
    y=games
    yAxisTitle="Games"
/>

### All Games

<DataTable
    data={games}
    search=true
    rows=25
/>
