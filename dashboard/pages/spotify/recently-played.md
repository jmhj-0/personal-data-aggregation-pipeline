# Recently Played

```sql recent
select
    played_at,
    track_name,
    artist_names,
    album_name,
    duration_secs
from personal_data.spotify_recently_played
order by played_at desc
```

```sql by_hour
select
    play_hour as hour,
    count(*) as plays
from personal_data.spotify_recently_played
group by play_hour
order by play_hour
```

```sql by_artist
select
    artist_names,
    count(*) as plays
from personal_data.spotify_recently_played
group by artist_names
order by plays desc
limit 10
```

<BarChart data={by_hour} x=hour y=plays yAxisTitle="Plays" title="Plays by Hour of Day" />

<BarChart data={by_artist} x=artist_names y=plays swapXY=true title="Most Played Artists (recent)" />

<DataTable data={recent} rows=50 />
