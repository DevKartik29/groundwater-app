import dataclasses
import sqlite3
from datetime import datetime

# Import the math functions we just built!
from analytics import calculate_trend, calculate_recharge, detect_anomalies, get_status

def run_refresh():
    conn = sqlite3.connect("groundwater.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Get all stations and their specific yield
    stations = cursor.execute("SELECT station_id, specific_yield FROM stations").fetchall()

    for st in stations:
        station_id = st["station_id"]
        sy = st["specific_yield"]

        # TODO: 1. Fetch all water_level_m_bgl and ts for this station from `readings`, ordered by ts ASC
        # Hint: rows = cursor.execute("SELECT ts, water_level_m_bgl FROM readings WHERE station_id=? ORDER BY ts ASC", (station_id,)).fetchall()
        rows = cursor.execute(
            "SELECT ts, water_level_m_bgl FROM readings WHERE station_id=? AND quality_flag = 'OK' ORDER BY ts ASC",
            (station_id,)
        ).fetchall()
            
        # TODO: 2. Extract dates and levels into two separate lists
        # Hint: dates = [row["ts"] for row in rows]
        #       levels = [row["water_level_m_bgl"] for row in rows]
        dates = [row["ts"] for row in rows]
        levels = [row["water_level_m_bgl"] for row in rows]
        
        
        # TODO: 3. Call our analytics functions
        # Hint: trend = calculate_trend(dates, levels)
        #       recharge = calculate_recharge(dates, levels, sy)
        #       anomalies = detect_anomalies(levels)
        #       status = get_status(trend)
        trend = calculate_trend(dates, levels)
        recharge = calculate_recharge(dates, levels, sy)
        anomalies = detect_anomalies(levels)
        status = get_status(trend)


        # TODO: 4. UPDATE the stations table with these new values
        # Hint: cursor.execute("""
        #           UPDATE stations 
        #           SET trend_m_per_year=?, recharge_mm=?, anomaly_count=?, status=?, last_refreshed=? 
        #           WHERE station_id=?
        #       """, (trend, recharge, anomalies, status, datetime.now().isoformat(), station_id))
        cursor.execute("""
        UPDATE stations
        SET trend_m_per_year=?,
            recharge_mm=?,
            anomaly_count=?,
            status=?,
            last_refreshed=?
            WHERE station_id=?
        """, (
            trend,
            recharge,
            anomalies,
            status,
            datetime.now().isoformat(),
         station_id
        ))
        # This will print our progress so we can watch it work!
        print(f"Refreshed {station_id}: Trend {trend}, Recharge {recharge}, Status {status}, Anomalies {anomalies}")
        pass

    # TODO: 5. Commit the changes and close the connection
    # Hint: conn.commit()
    #       conn.close()
    conn.commit()
    conn.close()
    print("Refresh complete!")

if __name__ == "__main__":
    run_refresh()
