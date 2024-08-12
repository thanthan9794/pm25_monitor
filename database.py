import sqlite3
from datetime import datetime
import logging

def init_db(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS pm25_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT,
                            device_id TEXT,
                            pm25 REAL,
                            program_run_time TEXT,
                            UNIQUE(timestamp, device_id))''')
            c.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp_device ON pm25_data (timestamp, device_id)''')
    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {e}")
        raise

def insert_data(db_path, data, device_id):
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            program_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            records = []
            for proj in data.get('feeds', [])[0]:
                for entry in data['feeds'][0].get(proj, []):
                    timestamp = list(entry.keys())[0]
                    record = entry[timestamp]
                    pm25 = record.get('s_d0', None)
                    records.append((timestamp, device_id, pm25, program_run_time))
            
            c.executemany("""
                INSERT OR IGNORE INTO pm25_data (timestamp, device_id, pm25, program_run_time) 
                VALUES (?, ?, ?, ?)
            """, records)
    except sqlite3.Error as e:
        logging.error(f"Database insertion error: {e}")
        raise