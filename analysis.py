from datetime import datetime
import pandas as pd
from database import get_data

def analyze_data(db_path, device_id):
    data = get_data(db_path)
    df = pd.DataFrame(data, columns=['id', 'timestamp', 'device_id', 'pm25', 'run_time'])
    
    # Filter by device_id
    device_df = df[df['device_id'] == device_id].copy()

    above_threshold = device_df[device_df['pm25'] > 30]['timestamp'].tolist()
    
    # Convert timestamp to datetime and extract date
    device_df['date'] = pd.to_datetime(device_df['timestamp']).dt.date

    # Group by date to get daily stats
    daily_stats = device_df.groupby('date')['pm25'].agg(['max', 'min', 'mean']).reset_index()
    daily_stats.rename(columns={'max': 'max_pm25', 'min': 'min_pm25', 'mean': 'avg_pm25'}, inplace=True)

    return {'above_threshold': above_threshold, 'daily_stats': daily_stats}