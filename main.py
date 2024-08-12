import argparse
import logging
import os
from datetime import datetime
from pm25api import fetch_data
from database import init_db, insert_data
from analysis import analyze_data
from report import generate_report

API_URL = "https://pm25.lass-net.org/API-1.0.0/device/{device_id}/history/"

def main():
    parser = argparse.ArgumentParser(description="PM2.5 Monitor Program")
    parser.add_argument("-i", "--device_id", default="08BEAC028630", help="Device ID to fetch data for. (default: %(default)s)")
    parser.add_argument("-t", "--threshold", default=30, help="PM2.5 danger threshold. (default: %(default)s)")
    parser.add_argument("-d", "--database_path", default='pm25_data.db', help="Database name. (default: %(default)s)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting PM2.5 Monitor Program")

    device_id = args.device_id
    threshold = args.threshold
    db_path = args.database_path

    # input validation
    if not isinstance(threshold, (int, float)):
        raise ValueError('Invalid threshold input')
    if db_path[-3:] != '.db':
        raise ValueError('Invalid database path')

    try:
        # Fetch data from API
        logging.info(f"Fetching data for device ID: {device_id}")
        data = fetch_data(API_URL, device_id)

        # Save data to database
        logging.info("Inserting data into database")
        insert_data(db_path, data, device_id)

        # Analyze data
        logging.info("Analyzing data")
        analysis_results = analyze_data(db_path, device_id, threshold)

        # Generate report
        logging.info("Generating report")
        report = generate_report(analysis_results)

        # Save report as text file 
        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        report_filename = f"{output_dir}/{device_id}_{datetime.now().strftime('%Y%m%dT%H%M%S')}.txt"

        with open(report_filename, 'w') as report_file:
            report_file.write(report)

        logging.info(f"Report saved as {report_filename}")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
