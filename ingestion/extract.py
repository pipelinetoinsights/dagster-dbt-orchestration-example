from ingestion.helpers import (
    extract_leaderboard_usernames,
    extract_player_stats,
    extract_game_data,
    get_latest_month,
    load_to_postgres,
    truncate_table,
)
from ingestion.db_config import get_pg_connection
import pandas as pd


def run_extract(limit: int = 50):
    usernames = extract_leaderboard_usernames(limit=limit)
    all_stats = []
    all_games = []

    for user in usernames:
        try:
            print(f"Processing {user}...")
            stats = extract_player_stats(user)
            archive_url = get_latest_month(user)
            games = extract_game_data(user, archive_url) if archive_url else []

            all_stats.append(stats)
            all_games.extend(games)

        except Exception as e:
            print(f"Failed for {user}: {e}")

    stats_df = pd.DataFrame(all_stats)
    games_df = pd.DataFrame(all_games)

    conn = get_pg_connection()

    # Idempotent load for stats (truncate + insert)
    truncate_table(conn, "chess_raw_stats")
    load_to_postgres(stats_df, "chess_raw_stats", conn)

    # Append new game data, deduplicated internally
    load_to_postgres(games_df, "chess_raw_games", conn)

    conn.close()
    print("✅ Extraction and loading complete.")


if __name__ == "__main__":
    run_extract()
