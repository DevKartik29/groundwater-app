# pyrefly: ignore [missing-import]
from fastapi import FastAPI
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