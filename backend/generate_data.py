import math
import random
from datetime import datetime, timedelta

def generate_station_data(station_id, start_date, trend_m_per_year, days=1095): # P3 Day 2: 3 years
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
        # Uncomment this once water_level is calculated:
        readings.append({
            "station_id": station_id,
            "ts": current_time.isoformat(),
            "water_level_m_bgl": round(water_level, 2)
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
                
            # TODO: 9. Generate the 3-year data
            # data = generate_station_data(station_id, start, trend_m_per_year, days=1095)
            data = generate_station_data(
                station_id,
                start,
                trend_m_per_year,
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
                    "OK",
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
    print(f"Inserted {len(all_readings)} readings into the database!")
