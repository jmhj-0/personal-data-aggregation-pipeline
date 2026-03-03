# Anime

```sql summary
select
    count(*) as total,
    count(*) filter (list_status = 'completed') as completed,
    count(*) filter (list_status = 'watching') as watching,
    count(*) filter (list_status = 'plan_to_watch') as plan_to_watch,
    count(*) filter (list_status = 'dropped') as dropped,
    round(avg(list_score) filter (list_score is not null), 2) as avg_score
from personal_data.mal_anime
```

```sql by_status
select list_status as status, count(*) as entries
from personal_data.mal_anime
group by list_status
order by entries desc
```

```sql top_rated
select title, list_score, mean_score, num_episodes, genres, finished_at
from personal_data.mal_anime
where list_status = 'completed' and list_score is not null
order by list_score desc, mean_score desc
limit 25
```

```sql currently_watching
select title, num_episodes_watched, num_episodes, watch_progress_pct, started_at
from personal_data.mal_anime
where list_status = 'watching'
order by started_at desc
```

<BigValue data={summary} value="total" title="Total Entries" />
<BigValue data={summary} value="completed" title="Completed" />
<BigValue data={summary} value="watching" title="Watching" />
<BigValue data={summary} value="avg_score" title="Avg Score" fmt="num2"/>

### By Status

<BarChart data={by_status} x=status y=entries />

### Top Rated (Completed)

<DataTable data={top_rated} rows=25 />

### Currently Watching

<DataTable data={currently_watching} />
