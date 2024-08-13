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
python main.py [-h] [-i DEVICE_ID] [-t THRESHOLD] [-d DATABASE_PATH]
```

Sample Device ID: 08BEAC028630 (default), 08BEAC0286D4, 08BEAC02869E

Output: Report containing the following information is saved in reports\
- a list of times when the level when above the danger threshold
- the daily maximum, daily minimum, and daily average pollution value

## Assumptions
1. API & Data assumptions: API endpoint is available, the return data is accurate, complete and in valid JSON format. The s_d0 key corresponds to PM2.5 values.
2.	Input Device ID assumptions: User will input a valid device ID, or that default device ID (‘08BEAC028630’) will always be a valid choice.
3.	Database assumptions: Sufficient diskspace for the SQLite database and no concurrent access.
4.	Environmental assumptions: The environment requirements are met including Python environment, libraries, and network access, and the timezone, and locale settings will not interfere with any datetime operations


## Future Improvements:
1.	API & Data validation
      - Implement a more robust error handling and data validation for API response
      - Consider handling API structure changes such as schema changes
2.	Extend device ID input
      - Validate input pattern
      - Accept multiple device IDs via CL arguments or via config file
3.	Database optimization
      - Consider using a more scalable database solution if the data volume is expected to grow, or if multiple users/devices will be handled concurrently
      - For large datasets, leverage database queries to improve performance
4.	Logging enhancements
      - Include more granular information such as status, error types, data size, specific steps completed and timestamps for each operation
      - Save the log results for monitoring and debugging
5.	Unit Test for each module, adding documentation

