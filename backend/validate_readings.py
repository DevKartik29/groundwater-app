"""P6 Day 2 validation: check P3's generated readings for data quality issues."""
import sqlite3
import json

conn = sqlite3.connect("groundwater.db")
cur = conn.cursor()

print("=" * 50)
print("P6 Day 2 — Readings Validation")
print("=" * 50)

# --------------------------------------------------
# CHECK 1: Null values in critical columns
# --------------------------------------------------
print("\n--- Check 1: Null values ---")

null_count = cur.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE water_level_m_bgl IS NULL OR ts IS NULL
""").fetchone()[0]

print(f"  Rows with NULL water_level or timestamp: {null_count}")
print(f"  {'PASS ✅' if null_count == 0 else 'FAIL ❌'}")


# --------------------------------------------------
# CHECK 2: Negative depths
# --------------------------------------------------
print("\n--- Check 2: Negative depths ---")

negative_count = cur.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE water_level_m_bgl < 0
""").fetchone()[0]

print(f"  Rows with negative depth: {negative_count}")
print(f"  {'PASS ✅' if negative_count == 0 else 'FAIL ❌'}")


# --------------------------------------------------
# CHECK 3: Orphan station IDs
# --------------------------------------------------
print("\n--- Check 3: Orphan station IDs ---")

orphan_count = cur.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE station_id NOT IN (
        SELECT station_id FROM stations
    )
""").fetchone()[0]

print(f"  Readings with unknown station_id: {orphan_count}")
print(f"  {'PASS ✅' if orphan_count == 0 else 'FAIL ❌'}")


# --------------------------------------------------
# CHECK 4: Timestamps outside expected range
# --------------------------------------------------
print("\n--- Check 4: Timestamps out of range ---")

out_of_range_count = cur.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE ts < '2023-06-01'
       OR ts >= '2026-06-01'
""").fetchone()[0]

print(f"  Readings outside expected range: {out_of_range_count}")
print(f"  {'PASS ✅' if out_of_range_count == 0 else 'FAIL ❌'}")


# --------------------------------------------------
# CHECK 5: broken_rows.json vs database
# --------------------------------------------------
print("\n--- Check 5: Fault injection vs database ---")

with open("data/broken_rows.json", "r") as f:
    broken_rows = json.load(f)

expected_fault_count = len(broken_rows)

actual_fault_count = cur.execute("""
    SELECT COUNT(*)
    FROM readings
    WHERE quality_flag != 'OK'
""").fetchone()[0]

print(f"  Faults in broken_rows.json: {expected_fault_count}")
print(f"  Faults in database:          {actual_fault_count}")

if expected_fault_count == actual_fault_count:
    print("  Fault count: PASS ✅")
else:
    print("  Fault count: FAIL ❌")


# --------------------------------------------------
# Final result
# --------------------------------------------------
all_pass = (
    null_count == 0
    and negative_count == 0
    and orphan_count == 0
    and out_of_range_count == 0
    and expected_fault_count == actual_fault_count
)

print("\n" + "=" * 50)

if all_pass:
    print("OVERALL RESULT: ALL CHECKS PASS ✅")
else:
    print("OVERALL RESULT: SOME CHECKS FAILED ❌")

print("=" * 50)

conn.close()