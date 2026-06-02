{{
    config(
        materialized='table'
    )
}}

-- Equivalent of customer_lifetime_value for music listening behaviour
SELECT
    user_name,

    -- Listening volume metrics
    COUNT(*)                                        AS total_listens,
    COUNT(DISTINCT recording_msid)                  AS unique_tracks_played,
    COUNT(DISTINCT artist_msid)                     AS unique_artists_played,
    COUNT(DISTINCT release_msid)                    AS unique_releases_played,
    COUNT(DISTINCT listen_date)                     AS active_listening_days,

    -- Time span metrics
    MIN(listened_at)                                AS first_listen,
    MAX(listened_at)                                AS last_listen,
    DATE_DIFF(
        DATE(MAX(listened_at)),
        DATE(MIN(listened_at)),
        DAY
    )                                               AS listening_lifespan_days,

    -- Engagement score (equivalent of customer_lifetime_value)
    -- ✅ FIXED — minimum 1 day prevents NULL
    ROUND(
        COUNT(*) * 1.0 /
        GREATEST(DATE_DIFF(
            DATE(MAX(listened_at)),
            DATE(MIN(listened_at)),
            DAY), 1)
    , 2)  AS avg_listens_per_day,
    
    -- Listening time preference
    APPROX_TOP_COUNT(time_of_day, 1)[OFFSET(0)].value   AS preferred_time_of_day,
    APPROX_TOP_COUNT(listen_day_of_week, 1)[OFFSET(0)].value AS preferred_day_of_week

FROM {{ ref('fact_listens') }}
GROUP BY user_name