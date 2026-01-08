"""Simple ingestion/simulator for incidents. Run this to add demo incidents to the DB."""
from .models import insert_incident


SAMPLE = [
(31.5204, 74.3587, 2, 'Accident on main road'),
(31.5350, 74.3570, 1, 'Slow traffic near mall'),
(31.5150, 74.3700, 3, 'Road blocked - heavy incident')
]


if __name__ == '__main__':
    for lat, lng, sev, desc in SAMPLE:
        insert_incident(lat, lng, sev, desc)
        print('Inserted demo incidents')