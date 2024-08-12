import sqlite3
from datetime import datetime
import logging

def analyze_data(db_path, device_id, threshold) -> dict:
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()

            # Fetch timestamps where PM2.5 is above the threshold
            above_threshold_query = """
                SELECT timestamp 
                FROM pm25_data 
                WHERE device_id = ? AND pm25 > ?
            """
            c.execute(above_threshold_query, (device_id, threshold))
            above_threshold = [row[0] for row in c.fetchall()]

            # Fetch daily statistics (max, min, avg) for each date
            daily_stats_query = """
                SELECT DATE(timestamp) as date, 
                       MAX(pm25) as max_pm25, 
                       MIN(pm25) as min_pm25, 
                       AVG(pm25) as avg_pm25 
                FROM pm25_data 
                WHERE device_id = ? 
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            """
            c.execute(daily_stats_query, (device_id,))
            daily_stats = []
            for row in c.fetchall():
                daily_stats.append({
                    'date': row[0],
                    'max_pm25': row[1],
                    'min_pm25': row[2],
                    'avg_pm25': row[3]
                })

        return {'above_threshold': above_threshold, 'daily_stats': daily_stats}

    except sqlite3.Error as e:
        logging.error(f"Database query error: {e}")
        raise
