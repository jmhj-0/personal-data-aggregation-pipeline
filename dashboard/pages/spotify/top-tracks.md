# Top Tracks

<Dropdown name=time_range>
    <DropdownOption value="short_term" valueLabel="Last 4 weeks" />
    <DropdownOption value="medium_term" valueLabel="Last 6 months" />
    <DropdownOption value="long_term" valueLabel="All time" />
</Dropdown>

```sql tracks
select
    rank,
    track_name,
    artist_names,
    album_name,
    duration_secs,
    popularity,
    explicit
from personal_data.spotify_top_tracks
where time_range = '${inputs.time_range.value}'
order by rank
```

<DataTable data={tracks} rows=50 />
