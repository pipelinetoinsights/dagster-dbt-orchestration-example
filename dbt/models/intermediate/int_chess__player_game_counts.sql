with game_stats as (

    select *
    from {{ ref('int_chess__game_stats') }}

),

aggregated as (

    select
        username,
        count(*) as total_games,
        count(distinct opponent) as unique_opponents,
        round(sum(score)::numeric, 2) as total_score,
        round(avg(score)::numeric, 2) as avg_score
    from game_stats
    group by username

)

select * from aggregated
