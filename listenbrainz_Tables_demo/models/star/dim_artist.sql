SELECT DISTINCT
    artist_msid,
    artist_name
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE artist_msid IS NOT NULL