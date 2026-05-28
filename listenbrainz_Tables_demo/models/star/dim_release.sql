SELECT DISTINCT
    release_msid,
    release_name
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE release_msid IS NOT NULL
