SELECT
    login,
    name,
    bio,
    public_repos,
    public_gists,
    followers,
    following,
    created_at::TIMESTAMPTZ AS created_at,
    updated_at::TIMESTAMPTZ AS updated_at,
    _loaded_at
FROM {{ source('raw', 'github_profile') }}
