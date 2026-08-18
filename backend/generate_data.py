import math
import random
import json
from datetime import datetime, timedelta

def generate_station_data(station_id, start_date, trend_m_per_year, secret_broken_list, days=1095): # P3 Day 2: 3 years
    # Base depth of the water table (metres below ground)
    base_depth = 15.0
    
    current_time = start_date
    end_time = start_date + timedelta(days=days)
    
    readings = []
    
    while current_time < end_time:
        day_of_year = current_time.timetuple().tm_yday
        seasonal_cycle = math.sin((day_of_year / 365.0) * 2 * math.pi)
        
        # --- NEW TREND LOGIC ---
        # TODO: 4. Calculate how many days have passed since start_date
        # Hint: (current_time - start_date).total_seconds() / 86400.0
        days_passed = (current_time - start_date).total_seconds() / 86400.0
        
        # TODO: 5. Calculate the trend_shift
        # Hint: trend_m_per_year * (days_passed / 365.0)
        trend_shift = trend_m_per_year * (days_passed / 365.0)
        
        # TODO: 6. Add trend_shift to water_level calculation below
        water_level = base_depth + seasonal_cycle + trend_shift + random.uniform(-0.1, 0.1)
        water_level = round(water_level, 2)
        ts_iso = current_time.isoformat()
        
        is_broken = False
        # --- P3 Day 3: INJECT FAULTS ---
        if random.random() < 0.05:
            is_broken = True
            fault_type = random.choice(["gap", "spike", "stuck"])
            
            if fault_type == "gap":
                secret_broken_list.append({
                    "station_id": station_id,
                    "ts": ts_iso,
                    "type": "gap"
                })
                current_time += timedelta(hours=6)
                continue
            elif fault_type == "spike":
                water_level = round(water_level * random.uniform(5, 10), 2)
                secret_broken_list.append({
                    "station_id": station_id,
                    "ts": ts_iso,
                    "type": "spike"
                })
            elif fault_type == "stuck":
                if len(readings) > 0:
                    water_level = readings[-1]["water_level_m_bgl"]
                secret_broken_list.append({
                    "station_id": station_id,
                    "ts": ts_iso,
                    "type": "stuck"
                })

        # TODO: Set quality_flag based on whether this reading is broken
        if is_broken:
            flag = fault_type.upper()   # "SPIKE" or "STUCK"
        else:
            flag = "OK"

        readings.append({
            "station_id": station_id,
            "ts": ts_iso,
            "water_level_m_bgl": water_level,
            "quality_flag": flag   # <-- NEW: carry the flag with each reading
        })
        
        current_time += timedelta(hours=6)
        
    return readings

if __name__ == "__main__":
    import csv
    import sqlite3
    
    # Set fixed random seed so test data doesn't change between runs
    random.seed(42)
    
    start = datetime(2023, 6, 1)
    all_readings = []
    
    # We will pass this empty list into our function to collect the broken row metadata
    secret_broken_list = []
    
    # P3 Day 5: Force specific trends for demo contrast
    DEMO_OVERRIDES = {
        "RJ-001": 1.5,    # steep decline — over-exploited aquifer
        "PB-002": -0.5    # clear recovery — successful intervention
    }
    
    # TODO: 7. Open and read 'data/stations.csv'
    # Hint: use the csv module. Skip the header row, then loop through the rest.
    
    # Inside your CSV loop:
    # station_id = row[0]
    with open("data/stations.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            station_id = row[0]
            
            # TODO: 8. Assign a random trend
            # Hint: Use random.random(). 
            # 20% chance -> recovering (random between -0.1 and -0.4)
            # 80% chance -> declining (random between 0.1 and 0.8)
            if random.random() < 0.2:
                trend_m_per_year = random.uniform(-0.4, -0.1)
            else:
                trend_m_per_year = random.uniform(0.1, 0.8)
            
            # P3 Day 5: Override trend for demo-contrast stations
            if station_id in DEMO_OVERRIDES:
                trend_m_per_year = DEMO_OVERRIDES[station_id]
                
            # TODO: 9. Generate the 3-year data
            # data = generate_station_data(station_id, start, trend_m_per_year, secret_broken_list, days=1095)
            data = generate_station_data(
                station_id,
                start,
                trend_m_per_year,
                secret_broken_list,
                days=1095
            )
            
            # TODO: 10. Append formatted tuples to all_readings
            # for r in data:
            #     all_readings.append((r["station_id"], r["ts"], r["water_level_m_bgl"], "OK", None))
            for r in data:
                all_readings.append((
                    r["station_id"],
                    r["ts"],
                    r["water_level_m_bgl"],
                    r["quality_flag"],   # Was hardcoded "OK" — now reads the actual flag
                    None
                ))
        
    # TODO: 11. Database Bulk Insert
    # - Connect to 'groundwater.db' using sqlite3
    # - Execute "DELETE FROM readings" to clear out any old test data
    # - Use executemany("INSERT INTO readings (station_id, ts, water_level_m_bgl, quality_flag, quality_reason) VALUES (?, ?, ?, ?, ?)", all_readings)
    # - Commit and close!
    conn = sqlite3.connect("groundwater.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM readings")
    cursor.executemany("INSERT INTO readings (station_id, ts, water_level_m_bgl, quality_flag, quality_reason) VALUES (?, ?, ?, ?, ?)", all_readings)
    conn.commit()
    conn.close()
    
    # TODO: 12. Save the secret answer key for P1!
    # Hint: Use json.dump to save secret_broken_list to "data/broken_rows.json"
    with open("data/broken_rows.json", "w") as f:
        json.dump(secret_broken_list, f, indent=2)
    
    print(f"Inserted {len(all_readings)} readings into the database!")
    print(f"Secretly injected {len(secret_broken_list)} faults!")
