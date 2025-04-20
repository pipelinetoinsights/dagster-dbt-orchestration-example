with base as (

    select *
    from {{ ref('stg_chess__raw_games') }}

),

scored as (

    select
        username,
        opponent,
        end_time,
        case
            when result = 'win' then 1.0
            when result = 'draw' then 0.5
            else 0.0
        end as score
    from base

),

aggregated as (

    select
        username,
        count(*) as total_games,
        count(distinct opponent) as unique_opponents,
        round(sum(score)::numeric, 2) as total_score,
        round(avg(score)::numeric, 2) as avg_score
    from scored
    group by username

)

select * from aggregated
