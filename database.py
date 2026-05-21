import sqlite3
import datetime

DB_NAME = "tracker.db"


class Database:
    def __init__(self):
        self.db_name = DB_NAME
        self.init_db()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.connect()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time_added TEXT NOT NULL,
                seconds INTEGER DEFAULT 0,
                date TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    # Tasks

    def get_all_tasks(self):
        conn = self.connect()
        rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_task_by_id(self, task_id):
        conn = self.connect()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_tasks_by_date(self, date_str):
        conn = self.connect()
        rows = conn.execute("SELECT * FROM tasks WHERE date = ?", (date_str,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_task(self, name):
        now = datetime.datetime.now()
        conn = self.connect()
        conn.execute(
            "INSERT INTO tasks (name, time_added, seconds, date) VALUES (?, ?, ?, ?)",
            (name, now.strftime("%H:%M"), 0, str(now.date()))
        )
        conn.commit()
        conn.close()

    def update_task_seconds(self, task_id, seconds):
        conn = self.connect()
        conn.execute("UPDATE tasks SET seconds = ? WHERE id = ?", (seconds, task_id))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = self.connect()
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    def delete_all_tasks(self):
        conn = self.connect()
        conn.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

    # Chat

    def save_message(self, sender, message):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        conn = self.connect()
        conn.execute(
            "INSERT INTO chat_history (sender, message, timestamp) VALUES (?, ?, ?)",
            (sender, message, now)
        )
        conn.commit()
        conn.close()

    def get_last_messages(self, limit=10):
        conn = self.connect()
        rows = conn.execute(
            "SELECT * FROM chat_history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]
