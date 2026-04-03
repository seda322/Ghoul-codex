import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        rank TEXT DEFAULT 'Новичок',
        nick_generated INTEGER DEFAULT 0,
        builds_generated INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adjectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nouns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT
    )
    """)

    conn.commit()
    conn.close()

def user_exists(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user

def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, rank, nick_generated, builds_generated FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user

def increment_nick_counter(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET nick_generated = nick_generated + 1
        WHERE username=?
    """, (username,))

    conn.commit()
    conn.close()

def get_words(table):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT word FROM {table}")
    words = [row[0] for row in cursor.fetchall()]

    conn.close()
    return words

import random

def generate_nickname():
    adjectives = get_words("adjectives")
    nouns = get_words("nouns")

    if not adjectives or not nouns:
        return "NoWords"

    return random.choice(adjectives) + random.choice(nouns)

def check_password(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result is None:
        return None  # пользователя нет

    return result[0] == password  # True / False