import sqlite3


def connect():
    return sqlite3.connect("leaderboard.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

##########################################################################

def player_exists(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM players WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def insert_player(username):
    if not player_exists(username):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        conn.commit()
        conn.close()

def update_score(username, new_score):
    conn = connect()
    cursor = conn.cursor()

    # getting the current score
    cursor.execute("SELECT score FROM players WHERE username = ?", (username,))
    result = cursor.fetchone()

    current_score = result[0]

    #  update only if we did better than the previous one
    if new_score > current_score:
        cursor.execute("""
            UPDATE players
            SET score = ?
            WHERE username = ?;
        """, (new_score, username))

    conn.commit()
    conn.close()


def get_top_players(limit=5):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, score
        FROM players
        ORDER BY score DESC
        LIMIT ?;
    """, (limit,))
    results = cursor.fetchall()
    conn.close()
    return results
