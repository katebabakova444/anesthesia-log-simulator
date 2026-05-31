import psycopg2
import psycopg2.extras
import json
from models import Session, Log
from typing import List, Dict

class LogRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return psycopg2.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    weight REAL,
                    asa_class TEXT,
                    anesthesia_type TEXT,
                    block_type TEXT,
                    protocol TEXT,
                    doses TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
            conn.commit()

    def save_orm(self, entry: Dict):
        session = Session()
        try:
            log = Log(
            name=entry["name"],
            age=entry["age"],
            weight=entry["weight"],
            asa_class=entry["asa_class"],
            anesthesia_type=entry["anesthesia_type"],
            block_type=entry["block_type"],
            protocol=entry["protocol"],
            doses=json.dumps(entry["doses"])
            )
            session.add(log)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def load_all(self) -> List[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM logs")
        return [dict(row) for row in cursor.fetchall()]

    def filter(self, filters: Dict) -> List[Dict]:
        base_query = "SELECT * FROM logs"
        values = []
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)
            base_query += " WHERE " + " AND ".join(conditions)

        with self._connect() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(base_query, values)
        return [dict(row) for row in cursor.fetchall()]

    def delete(self, log_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs WHERE id = %s", (log_id,))
            deleted = cursor.rowcount
            conn.commit()
        return deleted > 0
