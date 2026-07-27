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
            password_hash TEXT NOT NULL,
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

def create_player(username, password_hash):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO players (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
        (username, password_hash)
    )
    conn.commit()
    inserted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return inserted

def get_password_hash(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM players WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

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
