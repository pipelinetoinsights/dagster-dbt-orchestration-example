with games as (

    select *
    from {{ ref('stg_chess__raw_games') }}

),

stats as (

    select *
    from {{ ref('stg_chess__raw_stats') }}
),

enriched as (

    select
        g.username,
        g.opponent,
        g.result,
        g.time_class,
        g.eco,
        g.end_time,
        g.url,

        -- Standardised score field
        s.wins,

        s.losses,
        s.draws,
        s.time_per_move,
        s.stats_updated_at,
        case
            when g.result = 'win' then 1.0
            when g.result = 'draw' then 0.5
            else 0.0
        end as score

    from games as g
    left join stats as s on g.username = s.username

)

select * from enriched
