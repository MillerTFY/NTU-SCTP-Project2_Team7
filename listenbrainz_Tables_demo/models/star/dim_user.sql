SELECT DISTINCT
    user_name
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE user_name IS NOT NULL