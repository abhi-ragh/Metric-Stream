import sqlite3 as sql

def connect_db(date):
    conn = sql.connect(f"data/{date}.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        cpu REAL,
        mem REAL,
        disk REAL,
        bytes_recv REAL,
        bytes_send REAL
    );
    """)
    conn.commit()
    return conn