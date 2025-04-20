with counts as (

    select *
    from {{ ref('int_chess__player_game_counts') }}

),

stats as (

    select
        username,
        wins,
        losses,
        draws,
        time_per_move,
        stats_updated_at
    from {{ ref('int_chess__game_stats') }}

),

combined as (

    select
        c.username,
        c.total_games,
        c.unique_opponents,
        c.total_score,
        c.avg_score,
        s.wins,
        s.losses,
        s.draws,
        s.time_per_move,
        s.stats_updated_at
    from counts as c
    left join stats as s
        on c.username = s.username

)

select * from combined
