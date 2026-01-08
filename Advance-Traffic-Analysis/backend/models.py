import csv
import os
from datetime import datetime
from .config import CSV_FILE  # Path defined in config.py

# Define CSV headers
HEADERS = ["id", "lat", "lng", "severity", "description", "timestamp"]

# Initialize CSV file if it doesn’t exist
def init_db():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

# Insert a new incident record
def insert_incident(lat, lng, severity=1, description=None, timestamp=None):
    init_db()
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    # Count current rows to assign a new ID
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = list(csv.reader(file))
            next_id = len(reader)  # header counts as 1, so first row = id=1
    else:
        next_id = 1

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([next_id, lat, lng, severity, description, timestamp])
    return next_id

# Get recent incidents (latest N)
def get_incidents_recent(limit=500):
    init_db()
    with open(CSV_FILE, mode="r") as file:
        reader = list(csv.DictReader(file))
        # Return the last 'limit' rows (reverse order)
        return reader[-limit:][::-1]
