# Methodology — Groundwater Resource Evaluation

## 1. Overview

This application evaluates groundwater resources using Digital Water Level Recorder (DWLR) data from 30 monitoring stations across India. It computes three key metrics per station: **water-table trend**, **groundwater recharge**, and **data anomaly count**.

> **Important:** All water-level values are expressed as **depth below ground level (m bgl)**. A larger number means deeper water — i.e., worse conditions.

---

## 2. Data Source

- **Stations:** 30 CGWB monitoring wells from `data/stations.csv`, covering alluvial, basaltic, granitic, and limestone formations.
- **Readings:** 6-hourly synthetic DWLR data over 3 years (June 2023 – May 2026), generated with `backend/generate_data.py` using a fixed random seed (`seed=42`) for reproducibility.
- **Why synthetic?** The live WIMS feed is restricted to authorised agencies. Our data generator simulates realistic seasonal cycles (monsoon recharge + dry-season decline) with injected sensor faults, so every analytical function can be tested against known ground truth.

---

## 3. Trend Calculation

**File:** `backend/analytics.py` → `calculate_trend()`

**Method:** Ordinary least-squares linear regression (`numpy.polyfit`, degree 1) on all non-flagged daily-average readings.

**Steps:**
1. Convert each date to "days since first reading" (numeric x-axis).
2. Fit a straight line: `slope, intercept = np.polyfit(days, levels, 1)`.
3. The slope is in **metres per day** — multiply by **365.25** to get **metres per year**.

**Interpretation:**
- `trend > +0.1 m/yr` → **Declining** (water table falling)
- `trend < −0.1 m/yr` → **Recovering** (water table rising)
- Otherwise → **Stable**

> **Why positive = declining?** Because values are depth below ground. A positive slope means the depth number is increasing — i.e., the water is getting farther from the surface.

---

## 4. Recharge Estimation

**File:** `backend/analytics.py` → `calculate_recharge()`

**Method:** Water Table Fluctuation (WTF) method, the standard approach recommended by CGWB.

**Formula:**
```
Recharge (mm) = Δh × Sy × 1000
```

Where:
- **Δh** = `max(levels) − min(levels)` within the water year (1 June – 31 May). This captures the full seasonal swing from deepest (pre-monsoon) to shallowest (post-monsoon).
- **Sy** = Specific yield for the formation type, sourced from the `SPECIFIC_YIELD` dictionary in `backend/analytics.py`. These are standard textbook values, not site-specific measurements.

**Sanity check:** Recharge should typically be 5–25% of local annual rainfall. Values outside this range suggest either unusual hydrogeology or a data quality issue.

> **Precision note:** Specific yield is an approximate table value. Recharge figures should be treated as estimates, not precise measurements.

---

## 5. Anomaly Detection

**File:** `backend/analytics.py` → `detect_anomalies()`

**Method:** Adjacent-reading comparison to identify two types of sensor faults:

1. **Spikes:** `|level[i] − level[i−1]| > 2.0 m` — a physically implausible jump between consecutive readings.
2. **Stuck sensor:** `level[i] == level[i−1]` exactly — indicates the sensor is reporting a frozen value.

**Important:** Flagged readings are **never deleted**. They are marked with `quality_flag` in the database and excluded from trend and recharge calculations, but remain in the historical record for auditability.

---

## 6. Status Classification

**File:** `backend/analytics.py` → `get_status()`

Stations are classified based on their trend value:

| Trend (m/yr) | Status | Meaning |
|---|---|---|
| > +0.1 | **Declining** | Water table falling — attention needed |
| < −0.1 | **Recovering** | Water table rising — improving conditions |
| −0.1 to +0.1 | **Stable** | Within normal variance |
| No data | **Unknown** | Insufficient readings for trend calculation |

---

## 7. Architecture

```
generate_data.py  →  SQLite DB  ←  refresh.py (precomputes analytics)
                         ↓
                    FastAPI endpoints
                         ↓
              Frontend (Chart.js + Leaflet)
```

- **Precomputation:** `refresh.py` runs all analytics functions and stores results (`trend_m_per_year`, `recharge_mm`, `anomaly_count`, `status`) directly in the `stations` table. This avoids running 130,000+ calculations on every page load.
- **API contract:** Defined in `04_API_CONTRACT.md`. The `/analytics` endpoint serves precomputed values; the `/timeseries` endpoint serves raw daily averages with quality flags.

---

## 8. Limitations

1. **Synthetic data.** Real DWLR data would show more complex patterns (pump interference, irregular monsoon onset, spatial correlation between nearby wells).
2. **Table-value Sy.** Specific yield varies within a formation. Site-specific pumping tests would give more accurate recharge estimates.
3. **Simple anomaly detection.** Production systems use statistical methods (z-scores, isolation forests) rather than fixed thresholds.
4. **No forecasting.** The app reports historical trends only. Time-series forecasting (SARIMA, LSTM) is a natural extension but was scoped out.
5. **Single water year.** Recharge is computed for the most recent water year only. Multi-year averaging would smooth out anomalous years.
