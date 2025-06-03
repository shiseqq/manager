import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            timestamp TEXT,
            cpu REAL,
            ram REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_stats(cpu, ram):
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stats VALUES (?, ?, ?)",
        (datetime.now().isoformat(), cpu, ram)
    )
    conn.commit()
    conn.close()