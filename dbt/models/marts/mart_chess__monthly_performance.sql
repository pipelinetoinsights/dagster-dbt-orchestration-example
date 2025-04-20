with stats as (

    select *
    from {{ ref('int_chess__game_stats') }}

),

monthly_summary as (

    select
        username,
        date_trunc('month', end_time) as month,
        count(*) as total_games,
        sum(case when result = 'win' then 1 else 0 end) as wins,
        sum(case when result = 'draw' then 1 else 0 end) as draws,
        sum(case when result not in ('win', 'draw') then 1 else 0 end) as losses
    from stats
    group by username, date_trunc('month', end_time)

)

select * from monthly_summary
