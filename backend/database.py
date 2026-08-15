import sqlite3

def init_db():
    # 1. Connect to the local database file (created if it doesn't exist)
    conn = sqlite3.connect("groundwater.db")
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
        status              TEXT,
        last_refreshed      TEXT
    )
""")

    # 3. Execute raw SQL to create the readings table
    cursor.execute("""
        -- TODO: Copy the 'CREATE TABLE readings' SQL from 04_API_CONTRACT.md here
    """)

    # 4. Create the index for faster lookups
    cursor.execute("""
        -- TODO: Copy the 'CREATE INDEX' SQL from 04_API_CONTRACT.md here
    """)

    conn.commit()
    conn.close()
    print("Database built!")

if __name__ == "__main__":
    init_db()