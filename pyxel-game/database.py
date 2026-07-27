import sqlite3
import hashlib


def connect():
    return sqlite3.connect("leaderboard.db")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            score INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

######## ####### ####### ######## ####### ####### ####### ###### ###### ##### #####

def player_exists(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM players WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def create_player(username, password):
    if player_exists(username):
        return False
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO players (username, password_hash) VALUES (?, ?)",
        (username, hash_password(password))
    )
    conn.commit()
    conn.close()
    return True

def verify_password(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM players WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0] == hash_password(password)

def update_score(username, new_score):
    conn = connect()
    cursor = conn.cursor()

    # getting the current score
    cursor.execute("SELECT score FROM players WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return

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


def get_top_players(limit=3):
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
