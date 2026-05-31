{% snapshot track_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='recording_msid',
        strategy='timestamp',
        updated_at='listened_at',
    )
}}

SELECT
    recording_msid,
    track_name,
    artist_msid,
    release_msid,
    listened_at
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE recording_msid IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY recording_msid
    ORDER BY listened_at DESC
) = 1

{% endsnapshot %}