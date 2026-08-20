import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "groundwater.db"))

def init_db():
    # 1. Connect to the local database file (created if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Execute raw SQL to create the stations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        station_id      TEXT PRIMARY KEY,
        name            TEXT NOT NULL,
        state           TEXT,
        district        TEXT,
        lat             REAL NOT NULL,
        lon             REAL NOT NULL,
        formation       TEXT,
        specific_yield  REAL,
        latest_level_m_bgl  REAL,
        trend_m_per_year    REAL,
        recharge_mm         REAL,
        anomaly_count       INTEGER,
        status              TEXT,
        last_refreshed      TEXT
    )
""")

    # 3. Execute raw SQL to create the readings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        station_id          TEXT,
        ts                  TEXT,
        water_level_m_bgl   REAL NOT NULL,
        quality_flag        TEXT DEFAULT 'OK',
        quality_reason      TEXT,
        PRIMARY KEY (station_id, ts),
        FOREIGN KEY (station_id) REFERENCES stations(station_id)
    )
    """)

    # 4. Create the index for faster lookups
    cursor.execute("""
    CREATE INDEX idx_readings_station_ts ON readings(station_id, ts);
""")

    conn.commit()
    conn.close()
    print("Database built!")

if __name__ == "__main__":
    init_db()