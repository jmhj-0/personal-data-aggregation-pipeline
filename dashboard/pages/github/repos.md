# GitHub — Repositories

```sql summary
select
    count(*) as total_repos,
    sum(stargazers_count) as total_stars,
    sum(forks_count) as total_forks,
    count(distinct language) filter (language is not null and language != '') as languages_used
from personal_data.github_repos
where is_fork = false
```

```sql top_repos
select
    repo_name,
    language,
    stargazers_count,
    forks_count,
    pushed_at::date as last_pushed
from personal_data.github_repos
where is_fork = false
order by stargazers_count desc
limit 10
```

```sql by_language
select
    coalesce(language, 'Unknown') as language,
    count(*) as repos
from personal_data.github_repos
where is_fork = false
group by language
order by repos desc
```

```sql all_repos
select
    repo_name,
    description,
    language,
    stargazers_count,
    forks_count,
    is_fork,
    pushed_at::date as last_pushed,
    created_at::date as created
from personal_data.github_repos
order by pushed_at desc
```

<BigValue data={summary} value="total_repos" title="Own Repos" />
<BigValue data={summary} value="total_stars" title="Total Stars" />
<BigValue data={summary} value="total_forks" title="Total Forks" />
<BigValue data={summary} value="languages_used" title="Languages Used" />

### Top Repos by Stars

<BarChart
    data={top_repos}
    x=repo_name
    y=stargazers_count
    yAxisTitle="Stars"
    swapXY=true
/>

### Repos by Language

<BarChart
    data={by_language}
    x=language
    y=repos
    yAxisTitle="Repos"
    swapXY=true
/>

### All Repositories

<DataTable
    data={all_repos}
    search=true
    rows=25
/>
