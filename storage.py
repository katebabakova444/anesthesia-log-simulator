import csv
import os
import datetime
import sqlite3
def save_to_db(**kwargs):
    filename = kwargs.get("filename", "anesthesia.db")
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS logs (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT,
         name TEXT,
         age INTEGER,
         weight REAL,
         asa_class TEXT,
         anesthesia_type TEXT,
         propofol REAL,
         fentanyl REAL,
         sevoflurane REAL,
         drug TEXT,
         dosage TEXT,
         technique TEXT
         )
    """)
    columns = ["timestamp", "name", "age", "weight", "asa_class", "anesthesia_type", "propofol", "fentanyl",
               "sevoflurane", "drug", "dosage", "technique"]
    kwargs["timestamp"] = datetime.datetime.now().isoformat()
    values = tuple(kwargs.get(col, "") for col in columns)
    cursor.execute(
        f"INSERT INTO logs ({','.join(columns)}) VALUES ({','.join(['?']*len(columns))})",
        values
    )
    conn.commit()
    conn.close()

def load_logs():
    conn = sqlite3.connect("anesthesia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def load_filtered_logs(filters):
    conn = sqlite3.connect("anesthesia.db")
    cursor = conn.cursor()

    base_query = "SELECT * FROM LOGS"
    values = []
    if filters:
        conditions = []
        for key, value in filters.items():
            conditions.append(f"{key} = ?")
            values.append(value)
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, values)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


