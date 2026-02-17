# db.py
import sqlite3
from datetime import datetime

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            referred_by INTEGER,
            first_visit TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username=None, referrer_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()

    if not exists:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO users (user_id, referred_by, first_visit) VALUES (?, ?, ?)",
            (user_id, referrer_id, now)  # <- исправлено на referrer_id
        )
        conn.commit()

    conn.close()
