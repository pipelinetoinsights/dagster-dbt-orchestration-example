with source as (

    select *
    from {{ source('raw', 'chess_raw_games') }}

),

renamed as (

    select
        username,
        opponent,
        result,
        time_class,
        eco,
        end_time,
        url
    from source

)

select * from renamed
