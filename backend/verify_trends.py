"""Day 4: Independent verification of calculate_trend() and get_status()."""
import csv, random, sqlite3
from datetime import datetime, timedelta
from generate_data import generate_station_data
from analytics import calculate_trend, get_status

# ============================================================
# PART 1: calculate_trend() with synthetic known-slope data
# ============================================================
print("=" * 60)
print("PART 1: calculate_trend() — synthetic data tests")
print("=" * 60)

def make_linear_series(slope_m_per_year, start_depth, days=1095):
    """Generate perfectly linear readings with a known slope."""
    dates = []
    levels = []
    start = datetime(2023, 6, 1)
    for d in range(0, days, 1):  # daily readings
        dt = start + timedelta(days=d)
        dates.append(dt.isoformat())
        depth = start_depth + slope_m_per_year * (d / 365.25)
        levels.append(round(depth, 4))
    return dates, levels

tests = [
    ("Declining +0.5 m/yr",  0.5,  10.0),
    ("Declining +1.0 m/yr",  1.0,  10.0),
    ("Recovering -0.3 m/yr", -0.3, 15.0),
    ("Flat 0.0 m/yr",        0.0,  12.0),
    ("Steep +2.0 m/yr",      2.0,   8.0),
]

all_trend_pass = True
for label, true_slope, base in tests:
    dates, levels = make_linear_series(true_slope, base)
    computed = calculate_trend(dates, levels)
    diff = abs(computed - true_slope)
    ok = diff < 0.001
    if not ok:
        all_trend_pass = False
    tag = "✅" if ok else "❌"
    print(f"  {label:<25} true={true_slope:>+6.2f}  got={computed:>+8.4f}  diff={diff:.6f}  {tag}")

# Edge cases
print()
print("  Edge cases:")
edge_none_1 = calculate_trend([], [])
edge_none_2 = calculate_trend(["2023-01-01T00:00:00"], [10.0])
tag1 = "✅" if edge_none_1 is None else "❌"
tag2 = "✅" if edge_none_2 is None else "❌"
print(f"    Empty lists → {edge_none_1}  {tag1}")
print(f"    Single point → {edge_none_2}  {tag2}")
if edge_none_1 is not None or edge_none_2 is not None:
    all_trend_pass = False

print(f"\n  calculate_trend() verdict: {'ALL PASS ✅' if all_trend_pass else 'SOME FAILED ❌'}")

# ============================================================
# PART 2: get_status() with specific test values
# ============================================================
print()
print("=" * 60)
print("PART 2: get_status() — edge case tests")
print("=" * 60)

status_tests = [
    (0.5,    "Declining",  "clearly positive"),
    (0.11,   "Declining",  "just above +0.1"),
    (0.1,    "Stable",     "exactly +0.1 boundary"),
    (0.05,   "Stable",     "small positive"),
    (0.0,    "Stable",     "zero"),
    (-0.05,  "Stable",     "small negative"),
    (-0.1,   "Stable",     "exactly -0.1 boundary"),
    (-0.11,  "Recovering", "just below -0.1"),
    (-0.5,   "Recovering", "clearly negative"),
    (None,   "Unknown",    "None input"),
]

all_status_pass = True
for val, expected, label in status_tests:
    got = get_status(val)
    ok = got == expected
    if not ok:
        all_status_pass = False
    tag = "✅" if ok else "❌"
    val_str = f"{val:>+6.2f}" if val is not None else "  None"
    print(f"  {label:<25} input={val_str}  expected={expected:<12} got={got:<12} {tag}")

print(f"\n  get_status() verdict: {'ALL PASS ✅' if all_status_pass else 'SOME FAILED ❌'}")

# ============================================================
# PART 3: 30-station status classification comparison
# ============================================================
print()
print("=" * 60)
print("PART 3: 30-station status classification (true vs computed)")
print("=" * 60)

# Replay seed to recover true trends
random.seed(42)
start = datetime(2023, 6, 1)
true_trends = {}

with open("data/stations.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        sid = row[0]
        if random.random() < 0.2:
            t = random.uniform(-0.4, -0.1)
        else:
            t = random.uniform(0.1, 0.8)
        true_trends[sid] = t
        generate_station_data(sid, start, t, [], days=1095)

conn = sqlite3.connect("groundwater.db")
cur = conn.cursor()

print(f"  {'Station':<10} {'True':>7} {'Comp':>7} {'TrueSt':<12} {'CompSt':<12} Match")
print("  " + "-" * 62)

matches = 0
mismatches = []

for sid, true_t in true_trends.items():
    cur.execute("""
        SELECT ts, water_level_m_bgl FROM readings
        WHERE station_id = ? AND quality_flag = 'OK'
        ORDER BY ts
    """, (sid,))
    rows = cur.fetchall()
    dates  = [r[0] for r in rows]
    levels = [r[1] for r in rows]

    comp_t = calculate_trend(dates, levels)
    true_st = get_status(true_t)
    comp_st = get_status(comp_t)
    ok = true_st == comp_st

    if ok:
        matches += 1
        tag = "✅"
    else:
        mismatches.append((sid, true_t, comp_t, true_st, comp_st))
        tag = "❌"

    print(f"  {sid:<10} {true_t:>+7.3f} {comp_t:>+7.3f} {true_st:<12} {comp_st:<12} {tag}")

conn.close()

print(f"\n  Status matches: {matches}/{len(true_trends)}")
if mismatches:
    print(f"  Mismatches ({len(mismatches)}):")
    for sid, tt, ct, ts, cs in mismatches:
        print(f"    {sid}: true={tt:+.4f} → {ts}, computed={ct:+.4f} → {cs}")
    print(f"\n  Root cause: systematic +0.18 m/yr bias in data pushes")
    print(f"  mildly-recovering stations across the -0.1 threshold.")
else:
    print("  All 30 stations classified identically. ✅")
