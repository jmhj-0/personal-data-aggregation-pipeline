SELECT
    repo_id,
    name AS repo_name,
    full_name,
    description,
    language,
    stargazers_count,
    forks_count,
    is_fork,
    is_private,
    created_at::TIMESTAMPTZ AS created_at,
    pushed_at::TIMESTAMPTZ AS pushed_at,
    topics,
    _loaded_at
FROM {{ source('raw', 'github_repos') }}
