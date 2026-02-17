# db.py
import sqlite3
from datetime import datetime

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        referrer_id INTEGER,
        first_visit_at TEXT
    )
    """)
    conn.commit()


def add_user(user_id, username, referrer_id=None):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    cursor.execute("""
    INSERT OR IGNORE INTO users 
    (user_id, username, referrer_id, first_visit_at)
    VALUES (?, ?, ?, ?)
    """, (user_id, username, referrer_id, now))

    conn.commit()
