# 04 — API Contract & Database

**5 endpoints. 2 tables. Freeze it on Day 1.**

This file is the seam between the backend half of the team (P1, P2, P3) and the frontend half (P4, P5). Once agreed, P2 builds *to* it and P4/P5 build *against* it — neither waits for the other.

Owner: **P1** · Built by: **P2** · Used by: **P4, P5**

---

## Database — two tables

```sql
CREATE TABLE stations (
    station_id      TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    state           TEXT,
    district        TEXT,
    lat             REAL NOT NULL,
    lon             REAL NOT NULL,
    formation       TEXT,          -- alluvium_sandy | alluvium_silty | sandstone
                                   -- | weathered_granite | basalt
    specific_yield  REAL,          -- filled at load time from analytics.SPECIFIC_YIELD

    -- precomputed by refresh.py on Day 4; NULL until then
    latest_level_m_bgl  REAL,
    trend_m_per_year    REAL,
    status              TEXT,      -- safe | watch | critical
    last_refreshed      TEXT
);

CREATE TABLE readings (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id          TEXT NOT NULL,
    ts                  TEXT NOT NULL,      -- "2026-08-14T06:00:00"
    water_level_m_bgl   REAL NOT NULL,      -- depth below ground. BIGGER = WORSE.
    quality_flag        TEXT DEFAULT 'OK',  -- OK | SPIKE | STUCK
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);

CREATE INDEX idx_readings_station_ts ON readings(station_id, ts);
```

**Four things to actually understand here, not just copy:**

- **The index.** Without it, "give me one station's last year" scans all 131,400 rows on every request. With it, SQLite jumps straight to that station's rows. Add it, then time the same query with and without — feeling the difference yourself is worth more than being told about it.
- **`specific_yield` is derived, not entered.** `stations.csv` carries only the `formation` name. P2 fills this column at load time by looking the formation up in `analytics.SPECIFIC_YIELD`. **One source of truth.** If the number lived in the CSV *and* in the code, they'd eventually disagree and nobody would know which one the app used.
- **The three precomputed columns.** `refresh.py` (Day 4) computes each station's status once and stores it. `/api/stations` then becomes one instant query instead of running the analytics 30 times per page load.
- **`quality_flag`.** We **never delete** a bad reading — we label it and keep it. Deleting destroys the record of what the sensor actually reported, and being able to say "we found 44 faulty readings, here they are" is worth more than a clean-looking chart.

**Timestamps are naive local time (IST), stored as ISO strings.** No timezone handling — a deliberate simplification, since all our data is Indian. Say so if asked; don't pretend it's more sophisticated than it is.

---

## Conventions

- All water levels are **metres below ground level**. The field name always says so: `water_level_m_bgl`.
- Base URL locally: `http://127.0.0.1:8000`
- The frontend keeps the base URL in **one place**, `frontend/shared.js`:
  ```js
  const API = "http://127.0.0.1:8000";   // change this one line when we deploy
  ```
- If a value can't be computed, return `null` **plus a `status` field explaining why**. Never `0` — a zero looks like a real measurement and somebody will believe it.

---

## 1. `GET /api/health`

```json
{ "status": "ok", "station_count": 30, "reading_count": 131400 }
```

Use this as your first test of everything: the server runs, the database is connected, and the data actually loaded.

---

## 2. `GET /api/stations`

Everything the map needs, in one call.

```json
[
  {
    "station_id": "PB-001",
    "name": "Ludhiana Piezometer 2",
    "state": "Punjab",
    "district": "Ludhiana",
    "lat": 30.9010,
    "lon": 75.8573,
    "latest_level_m_bgl": 24.8,
    "trend_m_per_year": 0.62,
    "status": "critical"
  }
]
```

`status` is `"safe"` | `"watch"` | `"critical"`, from the rules in `01_BRIEF_AND_SCIENCE.md` §6d.

> **Before Day 4, `latest_level_m_bgl`, `trend_m_per_year` and `status` will be `null`** — `refresh.py` doesn't exist yet. **P5: handle null by drawing the marker grey.** Don't wait for Day 4 to start; just make grey the default.

> **P5: this one call gives you everything for every marker** — position, colour, and popup text. Don't call the API once per station. Thirty requests where one would do is the most common beginner mistake with APIs, and it's visibly slower.

---

## 3. `GET /api/stations/{station_id}`

```json
{
  "station_id": "PB-001",
  "name": "Ludhiana Piezometer 2",
  "state": "Punjab",
  "district": "Ludhiana",
  "lat": 30.9010,
  "lon": 75.8573,
  "formation": "alluvium_sandy",
  "specific_yield": 0.14,
  "reading_count": 4380,
  "record_start": "2023-08-15T00:00:00",
  "record_end": "2026-08-14T18:00:00"
}
```

Unknown station → `404` with `{"detail": "Station not found"}`.

---

## 4. `GET /api/stations/{station_id}/timeseries?days=365`

**Daily averages, not raw 6-hourly readings.** A year of raw data is 1,460 points — sluggish to draw and unreadable. Averaging happens in SQL, where it's cheap:

```sql
SELECT DATE(ts) AS date,
       AVG(water_level_m_bgl) AS value,
       SUM(CASE WHEN quality_flag != 'OK' THEN 1 ELSE 0 END) AS bad_count
FROM readings
WHERE station_id = ? AND ts >= ?
GROUP BY DATE(ts)
ORDER BY date;
```

```json
{
  "station_id": "PB-001",
  "unit": "m_bgl",
  "days": 365,
  "points": [
    { "date": "2025-08-15", "value": 24.10, "flagged": false },
    { "date": "2025-08-16", "value": 24.14, "flagged": false },
    { "date": "2025-08-17", "value": 4.02,  "flagged": true  }
  ]
}
```

`flagged: true` means that day contained at least one reading whose `quality_flag` wasn't `OK` (i.e. `bad_count > 0`).

A station with no readings in the window returns `{"points": []}` — **not** a 404. P4 shows the empty state.

> **P4: plot `value` with the y-axis REVERSED.** Chart.js:
> ```js
> options: { scales: { y: { reverse: true, title: { display: true, text: 'Depth (m bgl)' } } } }
> ```
> Draw flagged points in red so a viewer can see the sensor misbehaving. Do not hide them.

> **P4: read the station id from the URL.** `station.html?id=PB-001` →
> ```js
> const id = new URLSearchParams(window.location.search).get("id");
> ```
> If `id` is missing or unknown, show a friendly message and a link back to the map — don't let the page throw.

---

## 5. `GET /api/stations/{station_id}/analytics`

The endpoint that makes this a product rather than a chart viewer.

```json
{
  "station_id": "PB-001",
  "trend": {
    "status": "ok",
    "slope_m_per_year": 0.62,
    "direction": "falling",
    "message": "Water table is falling about 0.62 m per year."
  },
  "recharge": {
    "status": "ok",
    "water_year": "2025-26",
    "delta_h_m": 1.2,
    "specific_yield": 0.14,
    "recharge_mm": 168.0,
    "note": "Water Table Fluctuation method (deepest minus shallowest level in the water year). Specific yield is a standard value for this formation, not a site measurement — treat as approximate."
  },
  "anomalies": {
    "status": "ok",
    "total": 44,
    "spike_count": 12,
    "stuck_count": 32,
    "message": "44 of 4,380 readings (1.0%) look like sensor faults."
  },
  "overall_status": "critical"
}
```

Any block may instead return:
```json
{ "status": "not_enough_data", "reason": "Needs at least one full water year; this station has 4 months of records." }
```

> **P4: if `status` isn't `"ok"`, display the `reason` text.** Don't show a blank card and don't show `0`. "We can't compute this yet, and here's why" is more trustworthy than a fake number — and it's the difference between a demo that survives a hard question and one that doesn't.

The `note` on recharge exists for the same reason. Specific yield is the largest uncertainty in the whole calculation, and we say so on screen, in front of the judges.

**Field name warning:** the trend field is `slope_m_per_year` here but `trend_m_per_year` in `/api/stations`. **Pick one and make them the same.** P1 decides on Day 1 — two names for one number will cost somebody twenty confused minutes. *(Recommendation: use `trend_m_per_year` in both.)*

---

## Mock file (P2 writes this Day 1, before anything else)

`frontend/mock.json` — 3 stations, hand-written, matching `/api/stations` exactly.

```js
// Day 1-2:  const url = "./mock.json";
// Day 3:    const url = `${API}/api/stations`;
```

One line changes. That's the entire cost of never being blocked.

---

## Changes to this file

Anyone can ask. **P1 decides**, and announces it in the channel. Silent contract changes break two people's code without warning — on a 10-day timeline, an expensive kind of quiet.
