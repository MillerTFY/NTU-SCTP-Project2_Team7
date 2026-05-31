-- SELECT DISTINCT
--     artist_msid,
--     artist_name
-- FROM {{ source('listenbrainz_raw', 'listen') }}
-- WHERE artist_msid IS NOT NULL

SELECT
    artist_msid,
    artist_name
FROM (
    SELECT
        artist_msid,
        artist_name,
        ROW_NUMBER() OVER (
            PARTITION BY artist_msid
            ORDER BY listened_at DESC
        ) AS rn
    FROM {{ source('listenbrainz_raw', 'listen') }}
    WHERE artist_msid IS NOT NULL
)
WHERE rn = 1