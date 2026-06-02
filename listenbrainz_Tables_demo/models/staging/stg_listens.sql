{{
    config(
        materialized='table'
    )
}}

SELECT
    -- Keys
    listened_at,
    user_name,
    recording_msid,
    artist_msid,
    release_msid,

    -- Derived date fields (links to dim_date)
    DATE(listened_at)                           AS listen_date,
    EXTRACT(YEAR FROM listened_at)              AS listen_year,
    EXTRACT(MONTH FROM listened_at)             AS listen_month,
    EXTRACT(HOUR FROM listened_at)              AS listen_hour,
    FORMAT_DATE('%A', DATE(listened_at))        AS listen_day_of_week,

    -- Derived flags
    CASE
        WHEN EXTRACT(DAYOFWEEK FROM listened_at) IN (1, 7)
        THEN TRUE ELSE FALSE
    END                                         AS is_weekend,

    CASE
        WHEN EXTRACT(HOUR FROM listened_at) BETWEEN 6 AND 11  THEN 'Morning'
        WHEN EXTRACT(HOUR FROM listened_at) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN EXTRACT(HOUR FROM listened_at) BETWEEN 18 AND 21 THEN 'Evening'
        ELSE 'Night'
    END                                         AS time_of_day,

    -- Descriptive fields (denormalised for easy analysis)
    track_name,
    artist_name,
    release_name

FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE listened_at > TIMESTAMP '2000-01-01 00:00:00 UTC'
  AND release_msid IS NOT NULL