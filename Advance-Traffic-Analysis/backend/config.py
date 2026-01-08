import os
from dotenv import load_dotenv
from pathlib import Path

# Base directory of the backend
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables (optional)
load_dotenv(BASE_DIR / '.env')

# Google Maps API Key (if you still want map integration)
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# CSV file path for storing incidents
CSV_FILE = os.getenv('CSV_FILE', str(BASE_DIR / 'incidents.csv'))
