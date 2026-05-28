SELECT DISTINCT
    DATE(listened_at)                        AS date_key,
    EXTRACT(YEAR  FROM listened_at)          AS year,
    EXTRACT(MONTH FROM listened_at)          AS month,
    EXTRACT(DAY   FROM listened_at)          AS day,
    FORMAT_DATE('%A', DATE(listened_at))     AS day_of_week,
    FORMAT_DATE('%B', DATE(listened_at))     AS month_name
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE listened_at > TIMESTAMP '2000-01-01 00:00:00 UTC'