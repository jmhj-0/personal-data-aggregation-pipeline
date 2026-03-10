# X — Tweets

```sql profile
select
    followers_count,
    following_count,
    tweet_count
from personal_data.x_profile
limit 1
```

```sql engagement_summary
select
    count(*) as tweets_tracked,
    sum(like_count) as total_likes,
    sum(retweet_count) as total_retweets,
    sum(total_engagements) as total_engagements,
    round(avg(total_engagements), 1) as avg_engagements_per_tweet
from personal_data.x_tweets
```

```sql top_tweets
select
    text,
    created_at::date as date,
    like_count,
    retweet_count,
    reply_count,
    total_engagements
from personal_data.x_tweets
order by total_engagements desc
limit 10
```

```sql all_tweets
select
    text,
    created_at::date as date,
    like_count,
    retweet_count,
    reply_count,
    quote_count,
    total_engagements
from personal_data.x_tweets
order by created_at desc
```

<BigValue data={profile} value="followers_count" title="Followers" />
<BigValue data={profile} value="following_count" title="Following" />
<BigValue data={profile} value="tweet_count" title="Total Tweets" />
<BigValue data={engagement_summary} value="avg_engagements_per_tweet" title="Avg Engagements" fmt="num1" />

### Top Tweets by Engagement

<DataTable data={top_tweets} rows=10 />

### All Tweets (Last 100)

<DataTable
    data={all_tweets}
    search=true
    rows=25
/>
