import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def connect():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            score INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

######## ####### ####### ######## ####### ####### ####### ###### ###### ##### #####

def player_exists(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM players WHERE username = %s", (username,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def insert_player(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
        (username,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_score(username, new_score):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM players WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        conn.close()
        return

    current_score = result[0]

    if new_score > current_score:
        cursor.execute("""
            UPDATE players
            SET score = %s
            WHERE username = %s;
        """, (new_score, username))
        conn.commit()

    cursor.close()
    conn.close()


def get_top_players(limit=5):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, score
        FROM players
        ORDER BY score DESC
        LIMIT %s;
    """, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
