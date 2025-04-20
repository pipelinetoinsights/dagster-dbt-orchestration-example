with base as (

    select *
    from {{ ref('stg_chess__raw_games') }}

),

enriched as (

    select
        username,
        opponent,
        result,
        time_class,
        eco,
        end_time,
        url,

        -- Standardised score field
        case
            when result = 'win' then 1.0
            when result = 'draw' then 0.5
            else 0.0
        end as score

    from base

)

select * from enriched
