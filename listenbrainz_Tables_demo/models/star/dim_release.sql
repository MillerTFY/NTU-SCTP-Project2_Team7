-- SELECT DISTINCT
--     release_msid,
--     release_name
-- FROM {{ source('listenbrainz_raw', 'listen') }}
-- WHERE release_msid IS NOT NULL

SELECT
    release_msid,
    release_name
FROM (
    SELECT
        release_msid,
        release_name,
        ROW_NUMBER() OVER (
            PARTITION BY release_msid
            ORDER BY listened_at DESC
        ) AS rn
    FROM {{ source('listenbrainz_raw', 'listen') }}
    WHERE release_msid IS NOT NULL
)
WHERE rn = 1