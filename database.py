import sqlite3
from datetime import datetime

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pm25_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    device_id TEXT,
                    pm25 REAL,
                    program_run_time TEXT,
                    UNIQUE(timestamp, device_id))''')
    conn.commit()
    conn.close()

def insert_data(db_path, data, device_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for proj in data['feeds'][0]:
        for entry in data['feeds'][0][proj]:
            # Extract the key for the dynamic key 'Timestamp_value'
            timestamp = list(entry.keys())[0]
            record = entry[timestamp]
            pm25 = record.get('s_d0', None)
            program_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                c.execute("INSERT INTO pm25_data (timestamp, device_id, pm25, program_run_time) VALUES (?, ?, ?, ?)", (timestamp, device_id, pm25, program_run_time))
            except sqlite3.IntegrityError:
                pass  # Skip if the data already exists
                
    conn.commit()
    conn.close()

def get_data(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM pm25_data")
    rows = c.fetchall()
    conn.close()
    return rows
