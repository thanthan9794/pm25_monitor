import logging
import requests
import sqlite3
import json
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_data(API_URL, device_id) -> dict:
    url = API_URL.format(device_id=device_id)
    
    # disable SSL warning
    requests.packages.urllib3.disable_warnings()

    try:
        with requests.Session() as session:
            response = session.get(url, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data or 'feeds' not in data or not data['feeds']:
                raise ValueError("API response is missing expected data")
            return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON response: {e}")
        raise
    except ValueError as ve:
        logging.error(f"Unexpected API response format: {ve}")
        raise