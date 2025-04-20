with source as (

    select *
    from {{ source('raw', 'chess_raw_stats') }}

),

renamed as (

    select
        username,
        wins,
        losses,
        draws,
        time_per_move,
        timestamp as stats_updated_at
    from source

)

select * from renamed
