import numpy as np
from datetime import datetime

# Specific yield (Sy) values for different geological formations.
# This represents the drainable porosity of the aquifer.
# Sourced from standard Central Ground Water Board (CGWB) norms.
SPECIFIC_YIELD = {
    "alluvium_sandy": 0.16,
    "alluvium_silty": 0.12,
    "weathered_granite": 0.05,
    "sandstone": 0.12,
    "basalt": 0.06
}

def calculate_trend(dates: list[str], levels: list[float]) -> float | None:
    """
    Calculates the long-term trend in groundwater level.
    Returns the trend in metres per year. A positive value means the water
    level is falling (depth is increasing).
    Returns None if there is not enough data (less than 2 points).
    """
    if not dates or not levels or len(dates) < 2:
        return None
        
    # TODO: 1. Convert the first date string to a datetime object to use as our "Day 0"
    start_date = datetime.fromisoformat(dates[0])
    
    # TODO: 2. Create an empty list to hold the integer "days since start" values
    days_since_start = []
    
    # TODO: 3. Loop through all the dates
    for date_str in dates:
        current_date = datetime.fromisoformat(date_str)
        delta = current_date - start_date
        days_since_start.append(delta.days)
    
    # TODO: 4. Use numpy to calculate the line of best fit (a degree-1 polynomial)
    slope, intercept = np.polyfit(days_since_start, levels, 1)
    
    # TODO: 5. Convert the daily slope to a yearly slope and return it (rounded to 4 decimals)
    return round(slope * 365.25, 4)

def calculate_recharge(dates: list[str], levels: list[float], specific_yield: float) -> float | None:
    """
    Calculates the annual groundwater recharge in millimetres (mm).
    Formula: Recharge = (Max Depth - Min Depth) * Specific Yield * 1000
    Returns None if there is not enough data.
    """
    if not dates or not levels or len(levels) < 2:
        return None
    # TODO: 1. Find the maximum depth (deepest water level) in the levels list
    # Hint: deepest = max(levels)
    deepest = max(levels)
    # TODO: 2. Find the minimum depth (shallowest water level) in the levels list
    # Hint: shallowest = min(levels)
    shallowest = min(levels)
    # TODO: 3. Calculate delta_h (the difference between deepest and shallowest)
    # Hint: delta_h = deepest - shallowest
    delta_h = deepest -shallowest
    # TODO: 4. Apply the formula: delta_h * specific_yield * 1000
    # Hint: recharge_mm = delta_h * specific_yield * 1000
    recharge_mm = delta_h * specific_yield * 1000
    # TODO: 5. Return the recharge, rounded to 1 decimal place
    # Hint: return round(recharge_mm, 1)
    return round(recharge_mm, 1)

def detect_anomalies(levels: list[float]) -> int:
    """
    Scans a list of water levels and counts the number of anomalies.
    Anomalies are defined as:
    1. Spikes/Drops: An absolute change of > 2.0 metres from the previous reading.
    2. Stuck sensor: The exact same reading as the previous reading.
    Returns the total count of anomalous readings.
    """
    if not levels or len(levels) < 2:
        return 0
        
    # TODO: 1. Create a variable to keep track of the anomaly count (start at 0)
    # Hint: anomalies = 0
    anomalies = 0
    # TODO: 2. Loop through the levels using an index, starting at 1 (so we can look back at i-1)
    # Hint: for i in range(1, len(levels)):
    for i in range(1, len(levels)):
        # TODO: 3. Inside the loop, check if the absolute difference is > 2.0
        # Hint: if abs(levels[i] - levels[i-1]) > 2.0:
        #           anomalies += 1
        if abs(levels[i] - levels[i-1]) > 2.0:
            anomalies += 1
    # TODO: 4. Otherwise, check if the reading is exactly the same as the previous one
    # Hint: elif levels[i] == levels[i-1]:
    #           anomalies += 1
        elif levels[i] == levels[i-1]:
            anomalies += 1
    # TODO: 5. Return the final anomaly count
    # Hint: return anomalies
    return anomalies

def get_status(trend: float | None) -> str:
    """
    Categorizes the trend into "Declining", "Recovering", or "Stable".
    A trend > +0.1 m/year is Declining (water is getting deeper).
    A trend < -0.1 m/year is Recovering (water is getting shallower).
    Anything in between is Stable.
    If trend is None, returns "Unknown".
    """
    # TODO: 6. If trend is None, return "Unknown"
    if trend is None:
        return "Unknown"
    # TODO: 7. If trend > 0.1, return "Declining"
    if trend > 0.1:
        return "Declining"
    # TODO: 8. If trend < -0.1, return "Recovering"
    if trend < -0.1:
        return "Recovering"
    # TODO: 9. Otherwise, return "Stable"
    return "Stable"

if __name__ == "__main__":
    # TEST BLOCK
    # Let's invent a fake station that drops exactly 0.5m every year
    test_dates = [
        "2020-01-01T00:00:00",
        "2021-01-01T00:00:00",
        "2022-01-01T00:00:00"
    ]
    test_levels = [
        10.0, # Start at 10.0m deep
        10.5, # Dropped 0.5m in year 1
        11.0  # Dropped another 0.5m in year 2
    ]
    
    trend = calculate_trend(test_dates, test_levels)
    print(f"Calculated Trend: {trend} m/year (Expected: 0.5)")

    # TEST BLOCK 2: Recharge
    # Let's say the water level fluctuated between 10.0m (shallowest) and 11.2m (deepest)
    # So Δh = 1.2m. With a specific yield of 0.14, we expect 168.0 mm of recharge.
    test_levels_2 = [10.0, 10.8, 11.2, 10.4]
    
    recharge = calculate_recharge(test_dates, test_levels_2, 0.14)
    print(f"Calculated Recharge: {recharge} mm (Expected: 168.0)")

    # TEST BLOCK 3: Anomalies & Status
    # This array has a massive 5.0m spike at index 2, and a stuck sensor at index 4
    test_levels_3 = [10.0, 10.1, 15.1, 10.2, 10.2]
    
    anomalies = detect_anomalies(test_levels_3)
    print(f"Detected Anomalies: {anomalies} (Expected: 2)")
    
    status_1 = get_status(0.5)
    status_2 = get_status(-0.2)
    status_3 = get_status(0.05)
    print(f"Status (0.5): {status_1} (Expected: Declining)")
    print(f"Status (-0.2): {status_2} (Expected: Recovering)")
    print(f"Status (0.05): {status_3} (Expected: Stable)")
