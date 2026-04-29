import sqlite3
import random

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    #таблица стримеров
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL,
        avatar TEXT,
        youtube_channel_id TEXT,
        description TEXT
    )
    """)

    # таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        nicknames_generated INTEGER DEFAULT 0,
        builds_created INTEGER DEFAULT 0
    )
    """)

    # таблица слов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        type TEXT NOT NULL
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
    cursor.execute("SELECT username, nicknames_generated FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def increase_nickname_counter(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET nicknames_generated = nicknames_generated + 1
        WHERE username = ?
    """, (username,))
    conn.commit()
    conn.close()

def get_words_by_type(word_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM words WHERE type=?", (word_type,))
    words = [row[0] for row in cursor.fetchall()]
    conn.close()
    return words

def generate_nickname():
    prefixes = get_words_by_type("prefix")
    bases = get_words_by_type("base")
    suffixes = get_words_by_type("suffix")
    emotions = get_words_by_type("emotional")

    patterns = [
        lambda: random.choice(prefixes) + random.choice(bases),
        lambda: random.choice(emotions) + random.choice(bases),
        lambda: random.choice(emotions) + random.choice(suffixes),
    ]

    nickname = random.choice(patterns)()
    return nickname

def check_password(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None

    return result[0] == password

def fill_words():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    words = [
        ("zxc","prefix"),
        ("king","prefix"),
        ("less","suffix"),
        ("love","emotional"),
        ("hope","emotional"),
        ("ghost","base"),
        ("shadow","base"),
        ("player","base"),
        ("hunter","base"),
        ("demon","base"),
    ]

    cursor.executemany("INSERT INTO words(word,type) VALUES(?,?)", words)
    conn.commit()
    conn.close()

def add_player(nickname, avatar, youtube_channel_id, description=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (nickname, avatar, youtube_channel_id, description)
        VALUES (?, ?, ?, ?)
    """, (nickname, avatar, youtube_channel_id, description))
    conn.commit()
    conn.close()

def get_all_players():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    conn.close()
    return players

def get_player(player_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE id=?", (player_id,))
    player = cursor.fetchone()
    conn.close()
    return player

def clear_players():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def init_default_players():
    clear_players()

    default_players = [
        ("stariy bog", "/static/sprites/stariy.jpg", "UCVS-dKzMQezuO3lKOLYi_Yg", "СтАрЫЙ бОг соСет у лИзыЫ"),
        ("zxcursed", "/static/sprites/cursed.jpg", "UCzYGXbhpHuM-FFND1T67evw", "АааА КаакОЙ КУСред КласСНи"),
        ("rostislav_999", "/static/sprites/rostik.jpg", "UCV8FWrsL1iCAWGHkBKgj96w", "чТО сЛУЧиЛоСь"), 
        ("shishmyr", '/static/sprites/shishmyr.jpg', 'UCrkvyAzvGp4s8fZqdNUa6Sw', 'ВиСп Как СМысЛо жиЗни'),  
    ]
    
    for nickname, avatar, youtube_id, desc in default_players:
        try:
            add_player(nickname, avatar, youtube_id, desc)
            print(f"Добавлен игрок: {nickname}")
        except Exception as e:
            print("Ошибка")