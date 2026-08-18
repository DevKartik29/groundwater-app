import sqlite3

# Approximate annual rainfall (in mm) based on historical climate data
# since this is not stored in the project database per the P6 instructions.
RAINFALL_DATA = {
    "PB-001": 730,   # Ludhiana, Punjab
    "PB-002": 700,   # Amritsar, Punjab
    "PB-003": 400,   # Bathinda, Punjab
    "HR-001": 700,   # Karnal, Haryana
    "RJ-001": 600,   # Jaipur, Rajasthan
    "RJ-002": 300,   # Jodhpur, Rajasthan
    "RJ-003": 650,   # Alwar, Rajasthan
    "RJ-004": 250,   # Barmer, Rajasthan
    "MH-001": 700,   # Pune, Maharashtra (city average)
    "MH-002": 700,   # Nashik, Maharashtra
    "MH-003": 700,   # Aurangabad, Maharashtra
    "TN-001": 600,   # Coimbatore, Tamil Nadu
    "TN-002": 850,   # Madurai, Tamil Nadu
    "TN-003": 1200,  # Cuddalore, Tamil Nadu
    "WB-001": 1400,  # Nadia, West Bengal
    "WB-002": 1400,  # Murshidabad, West Bengal
    "UP-001": 1000,  # Lucknow, UP
    "UP-002": 1000,  # Varanasi, UP
    "BR-001": 1100,  # Patna, Bihar
    "GJ-001": 600,   # Rajkot, Gujarat
    "GJ-002": 600,   # Mehsana, Gujarat
    "AP-001": 1000,  # Nellore, AP
    "AP-002": 550,   # Anantapur, AP
    "TG-001": 800,   # Hyderabad, Telangana
    "TG-002": 800,   # Warangal, Telangana
    "KA-001": 900,   # Bengaluru, Karnataka
    "KA-002": 1200,  # Belagavi, Karnataka
    "MP-001": 900,   # Indore, MP
    "MP-002": 1000,  # Rewa, MP
    "OD-001": 1400,  # Khordha, Odisha
}

def run_sanity_check():
    conn = sqlite3.connect("groundwater.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    stations = cur.execute("""
        SELECT station_id, name, district, recharge_mm
        FROM stations
        ORDER BY station_id
    """).fetchall()

    print(f"{'ID':<8} | {'District':<15} | {'Recharge (mm)':<13} | {'Rainfall (mm)':<13} | {'% of Rain':<10} | {'Sanity (5-25%)'}")
    print("-" * 85)

    for st in stations:
        sid = st["station_id"]
        recharge = st["recharge_mm"]
        rain = RAINFALL_DATA.get(sid, 1000)
        
        # Guard against zero recharge if data is missing
        if recharge is None:
            pct = 0
        else:
            pct = (recharge / rain) * 100
            
        status = "✅ PASS" if 5 <= pct <= 25 else "❌ FAIL"
        
        print(f"{sid:<8} | {st['district']:<15} | {recharge:<13.1f} | {rain:<13} | {pct:>5.1f}%     | {status}")

    conn.close()

if __name__ == "__main__":
    run_sanity_check()
