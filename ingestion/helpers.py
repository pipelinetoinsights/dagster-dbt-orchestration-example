import requests
import pandas as pd
from datetime import datetime

def fetch_json(url):
    headers = {
        "User-Agent": "pipeline2insights-chess-data-bot/1.0 (contact: you@example.com)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_leaderboard_usernames(limit=50):
    data = fetch_json("https://api.chess.com/pub/leaderboards")
    return [entry['username'] for entry in data['live_blitz'][:limit]]

def get_latest_month(username):
    archives = fetch_json(f"https://api.chess.com/pub/player/{username}/games/archives").get("archives", [])
    return archives[-1] if archives else None

def extract_player_stats(username):
    stats_url = f"https://api.chess.com/pub/player/{username}/stats"
    stats = fetch_json(stats_url)

    blitz = stats.get("chess_blitz", {}).get("record", {})
    return {
        "username": username,
        "wins": blitz.get("win", 0),
        "losses": blitz.get("loss", 0),
        "draws": blitz.get("draw", 0),
        "time_per_move": blitz.get("time_per_move"),
        "timestamp": datetime.utcnow()
    }

def extract_game_data(username, archive_url):
    games = fetch_json(archive_url).get("games", [])
    game_rows = []
    for game in games:
        white = game.get("white", {})
        black = game.get("black", {})
        game_rows.append({
            "username": username,
            "opponent": black["username"] if white["username"] == username else white["username"],
            "result": white["result"] if white["username"] == username else black["result"],
            "time_class": game.get("time_class"),
            "eco": game.get("eco", "NA"),
            "end_time": pd.to_datetime(game.get("end_time", 0), unit="s"),
            "url": game.get("url")
        })
    return game_rows

def truncate_table(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE {table_name}")
    conn.commit()
    cur.close()

def load_to_postgres(df, table_name, conn, unique_key=None):
    cur = conn.cursor()
    for _, row in df.iterrows():
        columns = ','.join(row.index)
        values = ','.join(['%s'] * len(row))
        if table_name == "chess_raw_stats":
            sql = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({values})
            """
        elif table_name == "chess_raw_games":
            # Assume unique constraint: (username, end_time, url)
            sql = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({values})
                ON CONFLICT (username, end_time, url) DO NOTHING
            """
        cur.execute(sql, tuple(row))
    conn.commit()
    cur.close()
