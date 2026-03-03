# Top Artists

<Dropdown name=time_range>
    <DropdownOption value="short_term" valueLabel="Last 4 weeks" />
    <DropdownOption value="medium_term" valueLabel="Last 6 months" />
    <DropdownOption value="long_term" valueLabel="All time" />
</Dropdown>

```sql artists
select
    rank,
    artist_name,
    genres,
    popularity,
    followers
from personal_data.spotify_top_artists
where time_range = '${inputs.time_range.value}'
order by rank
```

<BarChart
    data={artists}
    x=artist_name
    y=popularity
    swapXY=true
    yAxisTitle="Popularity"
/>

<DataTable data={artists} rows=50 />
