# Personal Data Dashboard

```sql now_gaming
select
    game_name,
    last_played_at::date as last_played
from personal_data.steam_games
where last_played_at is not null
order by last_played_at desc
limit 1
```

```sql now_watching
select title, num_episodes_watched, num_episodes
from personal_data.mal_anime
where list_status = 'watching'
order by started_at desc
limit 1
```

```sql now_reading_book
select title, author
from personal_data.goodreads_books
where shelf = 'currently-reading'
limit 1
```

```sql now_track
select track_name, artist_names
from personal_data.spotify_top_tracks
where time_range = 'short_term' and rank = 1
```

```sql now_artist
select artist_name, genres
from personal_data.spotify_top_artists
where time_range = 'short_term' and rank = 1
```

## Right Now

<BigValue data={now_gaming} value="game_name" title="Last Game Played" />
<BigValue data={now_watching} value="title" title="Watching" />
<BigValue data={now_reading_book} value="title" title="Reading" />
<BigValue data={now_track} value="track_name" title="Top Track This Month" />
<BigValue data={now_artist} value="artist_name" title="Top Artist This Month" />

---

```sql steam_summary
select
    count(*) as games_owned,
    round(sum(playtime_hours), 0) as hours_played,
    sum(achievements_unlocked) as achievements_unlocked
from personal_data.steam_games
```

```sql top_games
select game_name, playtime_hours
from personal_data.steam_games
where playtime_hours > 0
order by playtime_hours desc
limit 10
```

## Steam

<BigValue data={steam_summary} value="games_owned" title="Games Owned" />
<BigValue data={steam_summary} value="hours_played" title="Hours Played" />
<BigValue data={steam_summary} value="achievements_unlocked" title="Achievements Unlocked" />

<BarChart data={top_games} x=game_name y=playtime_hours yAxisTitle="Hours" swapXY=true title="Top 10 Games by Playtime" />

[View all games →](/steam/games)

---

```sql spotify_summary
select count(*) as recent_plays
from personal_data.spotify_recently_played
```

```sql spotify_top5
select rank, track_name, artist_names, duration_secs
from personal_data.spotify_top_tracks
where time_range = 'short_term'
order by rank
limit 5
```

## Spotify

<BigValue data={now_track} value="track_name" title="Top Track (4 weeks)" />
<BigValue data={now_artist} value="artist_name" title="Top Artist (4 weeks)" />
<BigValue data={spotify_summary} value="recent_plays" title="Recent Plays Tracked" />

<DataTable data={spotify_top5} title="Top 5 Tracks This Month" />

[Top tracks →](/spotify/top-tracks) · [Top artists →](/spotify/top-artists) · [Recently played →](/spotify/recently-played)

---

```sql anime_summary
select
    count(*) filter (list_status = 'completed') as completed,
    count(*) filter (list_status = 'watching') as watching,
    round(avg(list_score) filter (list_score is not null), 2) as avg_score
from personal_data.mal_anime
```

```sql manga_summary
select
    count(*) filter (list_status = 'completed') as completed,
    count(*) filter (list_status = 'reading') as reading,
    round(avg(list_score) filter (list_score is not null), 2) as avg_score
from personal_data.mal_manga
```

## My Anime List

**Anime**

<BigValue data={anime_summary} value="completed" title="Completed" />
<BigValue data={anime_summary} value="watching" title="Watching" />
<BigValue data={anime_summary} value="avg_score" title="Avg Score" fmt="num2" />

[Full anime list →](/my-anime-list/anime)

**Manga**

<BigValue data={manga_summary} value="completed" title="Completed" />
<BigValue data={manga_summary} value="reading" title="Reading" />
<BigValue data={manga_summary} value="avg_score" title="Avg Score" fmt="num2" />

[Full manga list →](/my-anime-list/manga)

---

```sql books_summary
select
    count(*) filter (shelf = 'read') as books_read,
    count(*) filter (shelf = 'currently-reading') as reading,
    count(*) filter (shelf = 'to-read') as to_read,
    round(avg(user_rating) filter (user_rating is not null), 2) as avg_rating,
    sum(num_pages) filter (shelf = 'read' and num_pages is not null) as pages_read
from personal_data.goodreads_books
```

## Goodreads

<BigValue data={books_summary} value="books_read" title="Books Read" />
<BigValue data={books_summary} value="pages_read" title="Pages Read" fmt="num0" />
<BigValue data={books_summary} value="avg_rating" title="Avg Rating" fmt="num2" />
<BigValue data={now_reading_book} value="title" title="Currently Reading" />

[Full reading list →](/goodreads/books)

---

```sql github_summary
select
    count(*) filter (is_fork = false) as own_repos,
    sum(stargazers_count) filter (is_fork = false) as total_stars,
    max(pushed_at)::date as last_pushed
from personal_data.github_repos
```

## GitHub

<BigValue data={github_summary} value="own_repos" title="Repos" />
<BigValue data={github_summary} value="total_stars" title="Stars" />
<BigValue data={github_summary} value="last_pushed" title="Last Push" />

[All repositories →](/github/repos)

---

```sql x_summary
select
    followers_count,
    following_count
from personal_data.x_user
limit 1
```

```sql x_recent
select
    text,
    created_at::date as date,
    total_engagements
from personal_data.x_tweets
order by created_at desc
limit 5
```

## X

<BigValue data={x_summary} value="followers_count" title="Followers" />
<BigValue data={x_summary} value="following_count" title="Following" />

<DataTable data={x_recent} title="Recent Tweets" />

[All tweets →](/x/tweets)
