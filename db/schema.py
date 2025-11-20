import sqlite3 as sql

def connect_db(date):
    conn = sql.connect(f"data/{date}.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        cpu REAL,
        mem REAL,
        disk REAL,
        net_send REAL,
        net_recv REAL
    );
    """)
    conn.commit()
    return conn