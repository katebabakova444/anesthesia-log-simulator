import csv
import os
import datetime
import json
import sqlite3
def save_to_db(name, age, weight, asa_class, anesthesia_type, block_type, protocol, doses):
    conn = sqlite3.connect("anesthesia.db")
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
    if isinstance(protocol, list):
        protocol = "\n".join(protocol)
    doses_json = json.dumps(doses)

    cursor.execute("""
        INSERT INTO logs 
        (name, age, weight, asa_class, anesthesia_type, block_type, protocol, doses)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        weight,
        asa_class,
        anesthesia_type,
        block_type,
        protocol,
        json.dumps(doses)
    ))

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


