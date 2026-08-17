import csv
import sqlite3
from analytics import SPECIFIC_YIELD

def load_stations():
    conn = sqlite3.connect("groundwater.db")
    cursor = conn.cursor()
    
    # We'll keep a list of stations to bulk insert
    stations_data = []

    # TODO: 1. Open data/stations.csv using csv.reader
    # Hint: don't forget to next(reader) to skip the header!
    with open("data/stations.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            station_id, name, state, district, lat, lon, formation = row
            # Inside your loop for each row:
            # station_id, name, state, district, lat, lon, formation = row
            
            # TODO: 2. Map the specific yield
            # We must look up the 'formation' in the SPECIFIC_YIELD dictionary to get the numerical value.
            # Hint: yield_val = SPECIFIC_YIELD.get(formation, 0.10) # 0.10 is a safe fallback
            yield_val = SPECIFIC_YIELD.get(formation, 0.10)
            # TODO: 3. Append the tuple to stations_data
            # Look at the schema in 04_API_CONTRACT.md. The stations table has 12 columns.
            # We only have 8 values right now: the 7 from the CSV + specific_yield.
            # For the last 4 columns (latest_level_m_bgl, trend_m_per_year, status, last_refreshed), just pass None!
            # stations_data.append((station_id, name, state, district, float(lat), float(lon), formation, yield_val, None, None, None, None))
            stations_data.append((
                station_id,
                name,
                state,
                district,
                float(lat),
                float(lon),
                formation,
                yield_val,
                None,
                None,
                None,
                None
            ))
    # TODO: 4. Clear old data and Bulk Insert
    # cursor.execute("DELETE FROM stations")
    # cursor.executemany("INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", stations_data)
    cursor.execute("DELETE FROM stations")

    cursor.executemany(
        """
        INSERT INTO stations (
            station_id, name, state, district, lat, lon, 
            formation, specific_yield, latest_level_m_bgl, 
            trend_m_per_year, status, last_refreshed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        stations_data
    )
    
    conn.commit()
    conn.close()
    
    print(f"Loaded {len(stations_data)} stations into the database!")

if __name__ == "__main__":
    load_stations()
