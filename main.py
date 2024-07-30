import requests
import sqlite3
import json
import logging
from datetime import datetime
from database import init_db, insert_data, get_data
from analysis import analyze_data
from report import generate_report

API_URL = "https://pm25.lass-net.org/API-1.0.0/device/{device_id}/history/"

def fetch_data(device_id):
    url = API_URL.format(device_id=device_id)
    
    # disable ssl warning
    requests.packages.urllib3.disable_warnings()
    
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data from API")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting PM2.5 Monitor Program")

    device_id = input("Enter device ID (press enter to use default device '08BEAC028630'): ") or "08BEAC028630"
    db_path = "pm25_data.db"

    try:
        # Initialize database
        logging.info("Initializing database")
        init_db(db_path)

        # Fetch data from API
        logging.info(f"Fetching data for device ID: {device_id}")
        data = fetch_data(device_id)

        # Save data to database
        logging.info("Inserting data into database")
        insert_data(db_path, data, device_id)

        # Analyze data
        logging.info("Analyzing data")
        analysis_results = analyze_data(db_path, device_id)

        # Generate report
        logging.info("Generating report")
        report = generate_report(analysis_results)
        # print(report)

        # Save report to file
        report_filename = f"reports/{device_id}_{datetime.now().strftime('%Y%m%dT%H%M%S')}.txt"
        with open(report_filename, 'w') as report_file:
            report_file.write(report)

        logging.info(f"Report saved as {report_filename}")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
