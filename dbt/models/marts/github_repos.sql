SELECT
    repo_id,
    repo_name,
    full_name,
    description,
    language,
    stargazers_count,
    forks_count,
    is_fork,
    is_private,
    created_at,
    pushed_at,
    topics,
    _loaded_at
FROM {{ ref('stg_github__repos') }}
