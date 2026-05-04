import sqlite3
import os

DB_PATH = "database/deadlines.db"

def check_db():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM tasks WHERE done=0").fetchall()
    for r in rows:
        print(dict(r))
    conn.close()

if __name__ == "__main__":
    check_db()
