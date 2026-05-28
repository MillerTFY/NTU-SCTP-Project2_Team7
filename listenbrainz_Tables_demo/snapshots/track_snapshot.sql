{% snapshot track_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='recording_msid',
        strategy='timestamp',
        updated_at='listened_at',
    )
}}

SELECT DISTINCT
    recording_msid,
    track_name,
    artist_msid,
    artist_name,
    release_msid,
    release_name,
    listened_at
FROM {{ source('listenbrainz_raw', 'listen') }}
WHERE recording_msid IS NOT NULL

{% endsnapshot %}