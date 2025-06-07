import sqlite3

DB_PATH = "file_cache.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_cache (
            file_hash TEXT PRIMARY KEY,
            file_name TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def is_file_processed(cursor, file_hash):
    cursor.execute("SELECT 1 FROM file_cache WHERE file_hash = ?", (file_hash,))
    return cursor.fetchone() is not None

def mark_file_as_processed(cursor, file_hash, file_name):
    cursor.execute("INSERT OR IGNORE INTO file_cache (file_hash, file_name) VALUES (?, ?)", (file_hash, file_name))
    cursor.connection.commit()
