import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "deadlines.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Buat tabel jika belum ada."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                nama_tugas  TEXT    NOT NULL,
                deadline    TEXT    NOT NULL,   -- format: YYYY-MM-DD HH:MM
                mata_kuliah TEXT,
                notified_1d INTEGER DEFAULT 0,  -- sudah notif H-1?
                notified_1h INTEGER DEFAULT 0,  -- sudah notif H-1jam?
                done        INTEGER DEFAULT 0,  -- sudah selesai?
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


# ── CRUD ────────────────────────────────────────────────────────────────────

def tambah_tugas(user_id: int, nama_tugas: str, deadline: str, mata_kuliah: str = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (user_id, nama_tugas, deadline, mata_kuliah) VALUES (?,?,?,?)",
            (user_id, nama_tugas, deadline, mata_kuliah),
        )
        conn.commit()
        return cur.lastrowid


def list_tugas(user_id: int) -> list[dict]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM tasks WHERE user_id=? AND done=0 ORDER BY deadline ASC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def selesaikan_tugas(task_id: int, user_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE tasks SET done=1 WHERE id=? AND user_id=?",
            (task_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0


def hapus_tugas(task_id: int, user_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM tasks WHERE id=? AND user_id=?",
            (task_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0


def get_tugas_belum_notif(level: str) -> list[dict]:
    """Ambil tugas yang belum dinotifikasi untuk level tertentu (1d / 1h)."""
    col = f"notified_{level}"
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"SELECT * FROM tasks WHERE done=0 AND {col}=0"
        ).fetchall()
        return [dict(r) for r in rows]


def tandai_notif(task_id: int, level: str):
    col = f"notified_{level}"
    with get_connection() as conn:
        conn.execute(f"UPDATE tasks SET {col}=1 WHERE id=?", (task_id,))
        conn.commit()


def get_all_users() -> list[int]:
    """Ambil semua user_id unik yang pernah mendaftarkan tugas."""
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT user_id FROM tasks").fetchall()
        return [r[0] for r in rows]
