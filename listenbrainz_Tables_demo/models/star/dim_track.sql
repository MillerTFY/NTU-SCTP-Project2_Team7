SELECT
    recording_msid,
    track_name,
    artist_msid,
    release_msid
FROM {{ ref('track_snapshot') }}
WHERE dbt_valid_to IS NULL
