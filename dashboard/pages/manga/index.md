# Manga

```sql summary
select
    count(*) as total,
    count(*) filter (list_status = 'completed') as completed,
    count(*) filter (list_status = 'reading') as reading,
    count(*) filter (list_status = 'plan_to_read') as plan_to_read,
    count(*) filter (list_status = 'dropped') as dropped,
    round(avg(list_score) filter (list_score is not null), 2) as avg_score
from personal_data.mal_manga
```

```sql by_status
select list_status as status, count(*) as entries
from personal_data.mal_manga
group by list_status
order by entries desc
```

```sql top_rated
select title, media_type, list_score, mean_score, num_chapters, genres, finished_at
from personal_data.mal_manga
where list_status = 'completed' and list_score is not null
order by list_score desc, mean_score desc
limit 25
```

```sql currently_reading
select title, media_type, num_chapters_read, num_chapters, read_progress_pct, started_at
from personal_data.mal_manga
where list_status = 'reading'
order by started_at desc
```

<BigValue data={summary} value="total" title="Total Entries" />
<BigValue data={summary} value="completed" title="Completed" />
<BigValue data={summary} value="reading" title="Reading" />
<BigValue data={summary} value="avg_score" title="Avg Score" fmt="num2"/>

### By Status

<BarChart data={by_status} x=status y=entries />

### Top Rated (Completed)

<DataTable data={top_rated} rows=25 />

### Currently Reading

<DataTable data={currently_reading} />
