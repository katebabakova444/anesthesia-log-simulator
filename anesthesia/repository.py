import sqlite3
import json
from typing import List, Dict, Optional

class LogRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    weight REAL,
                    asa_class TEXT,
                    anesthesia_type TEXT,
                    block_type TEXT,
                    protocol TEXT,
                    doses TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """)
            conn.commit()
    def save(self, entry: Dict):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO logs
                (name, age, weight, asa_class, anesthesia_type, block_type, protocol, doses)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["name"],
                    entry["age"],
                    entry["weight"],
                    entry["asa_class"],
                    entry["anesthesia_type"],
                    entry["block_type"],
                    entry["protocol"],
                    json.dumps(entry["doses"])
                )
            )
            conn.commit()
    def load_all(self) -> List[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    def filter(self, filters: Dict) -> List[Dict]:
        base_query = "SELECT * FROM logs"
        values = []
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                values.append(value)
            base_query += " WHERE " + " AND ".join(conditions)

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(base_query, values)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    def delete(self, log_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            deleted = cursor.rowcount
            conn.commit()
        return deleted > 0
