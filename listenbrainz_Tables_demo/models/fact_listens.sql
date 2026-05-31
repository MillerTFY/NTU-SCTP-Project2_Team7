SELECT
    listened_at,
    user_name,
    recording_msid,
    artist_msid,
    release_msid,
    track_name,
    artist_name,
    release_name
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE listened_at > TIMESTAMP '2000-01-01 00:00:00 UTC'
  AND release_msid IS NOT NULL