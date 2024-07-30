# PM2.5 Monitor

This application monitors PM2.5 levels using data from the PM2.5 Open Data Portal.

## Requirements

- Python 3.x
- SQLite

## Setup

1. Install the required Python packages:

   ```sh
   pip install -r requirements.txt

## Usage

Run the main script to fetch data, analyze it, and generate a report:

   ```sh
python main.py
```

Input: Device ID

Output: Report containing the following information is saved in reports\
- a list of times when the level when above the danger threshold
- the daily maximum, daily minimum, and daily average pollution value


