import sqlite3 as sql

def connect_db():
    conn = sql.connect("data/metrics.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device TEXT DEFAULT 'agent',
        ts TEXT NOT NULL,
        cpu REAL,
        mem REAL,
        disk REAL,
        bytes_recv REAL,
        bytes_send REAL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_ts ON metrics(ts);")
    conn.commit()
    return conn