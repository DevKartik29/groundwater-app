# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# 1. Enable CORS so the frontend (which runs on a different port) can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real app we'd restrict this, but for dev we allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Helper function to open a database connection and return rows as dictionaries."""
    conn = sqlite3.connect("groundwater.db")
    # This magic line makes SQLite return rows as dictionaries instead of plain tuples!
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/health")
async def health_check():
    # TODO: 2. Connect to the database using the helper function above
    # conn = ...
    conn = get_db_connection()
    
    # TODO: 3. Query the counts
    # cursor = conn.cursor()
    # Execute a query to get the number of stations, e.g.: cursor.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    # Execute a query to get the number of readings
    cursor = conn.cursor()

    station_count = cursor.execute(
        "SELECT COUNT(*) FROM stations"
    ).fetchone()[0]

    reading_count = cursor.execute(
        "SELECT COUNT(*) FROM readings"
    ).fetchone()[0]
    
    # TODO: 4. Close the connection and return the dictionary exactly matching 04_API_CONTRACT.md
    # return {"status": "ok", "station_count": ..., "reading_count": ...}
    conn.close()

    return {
        "status": "ok",
        "station_count": station_count,
        "reading_count": reading_count
    }

@app.get("/api/stations")
async def get_stations():
    # TODO: 5. Connect to the database
    conn = get_db_connection()
    # TODO: 6. Query all stations from the `stations` table
    # Since we set conn.row_factory = sqlite3.Row, cursor.fetchall() will give us a list of dictionary-like objects!
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT * FROM stations"
    ).fetchall()
    # TODO: 7. Close the connection
    conn.close()
    # TODO: 8. Return the rows
    # Hint: you can just `return rows` and FastAPI will automatically convert the SQLite rows to a beautiful JSON list for you!
    return rows

@app.get("/api/stations/{station_id}/timeseries")
async def get_station_timeseries(station_id: str, days: int = 1095):
    # TODO: 9. Connect to the database
    conn = get_db_connection()
    
    # TODO: 10. Write the SQL query to GROUP BY date and get the daily average

    query = """
        SELECT
            DATE(ts) AS ts,
            AVG(water_level_m_bgl) AS water_level_m_bgl
        FROM readings
        WHERE station_id = ?
        GROUP BY DATE(ts)
        ORDER BY ts DESC
        LIMIT ?
    """

    cursor = conn.cursor()

    rows = cursor.execute(
        query,
        (station_id, days)
    ).fetchall()
    
    # TODO: 11. Close the connection and return the rows
    conn.close()
    return rows

@app.get("/api/stations/{station_id}/analytics")
async def get_station_analytics(station_id: str):
    # TODO: 1. Connect to the database
    # Hint: conn = get_db_connection()
    conn = get_db_connection()
    
    # TODO: 2. Query the station row by station_id
    # Hint: cursor = conn.cursor()
    #       row = cursor.execute("SELECT * FROM stations WHERE station_id=?", (station_id,)).fetchone()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM stations WHERE station_id=?",
        (station_id,)
    ).fetchone()
    
    # TODO: 3. Handle the 404 case if the station doesn't exist
    # Hint: if not row:
    #           raise HTTPException(status_code=404, detail="Station not found")
    if not row:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # TODO: 4. Close the database connection
    # Hint: conn.close()
    conn.close()
    # TODO: 5. Extract the precomputed values from the row
    # Hint: trend_val = row["trend_m_per_year"]
    #       recharge_val = row["recharge_mm"]
    #       sy = row["specific_yield"]
    #       anomalies_val = row["anomaly_count"]
    #       status_val = row["status"]
    trend_val = row["trend_m_per_year"]
    recharge_val = row["recharge_mm"]
    sy = row["specific_yield"]
    anomalies_val = row["anomaly_count"]
    status_val = row["status"]
    # TODO: 6. Check if analytics haven't been computed yet
    # Hint: if status_val is None:
    #           return {"status": "not_enough_data", "reason": "Needs at least one full water year."}
    if status_val is None:
        return {"status": "not_enough_data", "reason": "Needs at least one full water year."}
    
    # TODO: 7. Build the `trend` dictionary block
    direction = "falling" if trend_val > 0 else "recovering"
    trend_dict = {
        "status": "ok",
        "slope_m_per_year": round(trend_val, 2),
        "direction": direction,
        "message": f"Water table is {direction} about {round(abs(trend_val), 2)} m per year."
    }
    
    # TODO: 8. Build the `recharge` dictionary block
    delta_h = recharge_val / (sy * 1000) if sy else 0
    recharge_dict = {
        "status": "ok",
        "water_year": "2025-26",
        "delta_h_m": round(delta_h, 2),
        "specific_yield": sy,
        "recharge_mm": round(recharge_val, 1),
        "note": "Water Table Fluctuation method (approximate)."
    }
    
    # TODO: 9. Build the `anomalies` dictionary block
    anomalies_dict = {
        "status": "ok",
        "total": anomalies_val,
        "message": f"{anomalies_val} of 4,380 readings look like sensor faults."
    }
    
    # TODO: 10. Return the final, giant JSON object matching the contract!
    return {
        "station_id": station_id,
        "trend": trend_dict,
        "recharge": recharge_dict,
        "anomalies": anomalies_dict,
        "overall_status": status_val
    }
    pass
