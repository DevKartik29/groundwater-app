# PROGRESS.md

> Lives in the repo root. **The agent reads this at the start of every session** — keep it accurate or it'll work on the wrong thing.
> Everyone updates their own row. P1 updates the day gates.

**Key:** ⬜ not started · 🟨 doing · ✅ done · 🟥 blocked

---

## Right now

| | |
|---|---|
| **Day** | 0 |
| **Next gate** | All 6 have a merged PR + answered the 6 science questions |
| **Blocked on** | — |
| **Updated** | ____ by P_ |

---

## Day gates

| Day | Must be true by end of day | Status |
|---|---|---|
| 0 | 6/6 merged PRs · 6/6 science answers · repo + `.gitignore` + `backend/__init__.py` | ⬜ |
| 1 | `stations.csv` (30 rows) · `mock.json` · `SPECIFIC_YIELD` dict · map renders · a page prints names | ⬜ |
| 2 | DB has 30 stations + 131,400 readings · `/api/stations` returns real JSON · CORS on | ⬜ |
| 3 | **Map → click station → real hydrograph.** The whole path works. | ✅ |
| 4 | `refresh.py` run · map dots coloured · station page shows trend, recharge, anomalies | ✅ |
| 5 | Feature complete. **Freeze.** | ⬜ |
| 6 | Bugs fixed, CSS done, all empty/error states handled | ⬜ |
| 7 | Deployed and reachable — or a conscious decision to demo locally | ⬜ |
| 8 | README tested on a clean machine · deck drafted · `docs/methodology.md` written | ⬜ |
| 9 | Two timed dry runs · P6 demos solo · backup video recorded | ⬜ |
| 10 | Buffer | ⬜ |

> **Day 3 is the real gate.** If map → station → chart isn't working by then, stop adding anything and fix it. Everything after Day 3 is decoration on that one path.

---

## Task board

### P1 — Lead + Analytics
| Day | Task | Status |
|---|---|---|
| 1 | `04_API_CONTRACT.md` circulated · `analytics.py` signatures · **`SPECIFIC_YIELD` dict** (P2 needs it Day 2) · `frontend/shared.js` | ⬜ |
| 2 | `calculate_trend()` + test on a series with a known slope (check the ×365.25) | ✅ |
| 3 | `calculate_recharge()` + test (Δh 1.2 m × Sy 0.14 → 168 mm) | ✅ |
| 4 | `detect_anomalies()` + `get_status()`, checked against P3's broken rows | ✅ |
| 5 | Review everything · hunt the depth-vs-elevation bug · verify numbers by hand | ⬜ |
| 6 | Empty and error states across the app | ⬜ |
| 8 | `docs/methodology.md` | ⬜ |
| — | **Daily:** PR reviews within hours · run the evening merge · keep this file true | ⬜ |

### P2 — Backend API + Database
| Day | Task | Status |
|---|---|---|
| 1 | **`mock.json` first** · `database.py` (2 tables + index) | ✅ |
| 2 | Load `stations.csv`, fill `specific_yield` from P1's dict · `/api/health` · `/api/stations` · **CORS** | ✅ |
| 3 | `/api/stations/{id}` · `/timeseries` (daily averages via SQL) | ✅ |
| 4 | `refresh.py` (precompute status) · `/analytics` endpoint | ✅ |
| 5 | `flagged` in timeseries response · time every endpoint | ⬜ |
| 7 | Deploy to Render — **rebuild DB in the start command** | ⬜ |

### P3 — Data Generator
| Day | Task | Status |
|---|---|---|
| 1 | One station, one year, 6-hourly. **Plot it and look at it.** | ✅ |
| 2 | 30 stations × 3 years = 131,400 readings · **fixed random seed** · `executemany` | ✅ |
| 3 | Inject faults (stuck, spike, gap) · **keep the list of broken rows** · leave flags as OK | ✅ |
| 4 | **Verify P1's trend against the decline you built in** — you're the only one with ground truth | ✅ |
| 5 | Tune for demo contrast: one steeply declining, one recovering | ✅ |

### P4 — Station Page + Charts *(beginner)*
| Day | Task | Status |
|---|---|---|
| 0–1 | JS + DOM basics · page that `fetch`es `mock.json` and prints names | ✅ |
| 2 | `station.html` + Chart.js line chart, **y-axis reversed** (P1 verifies) | ✅ |
| 3 | Switch to real API · read station id via `URLSearchParams` · real data | ✅ |
| 4 | Show trend, recharge, latest reading, anomaly count | ✅ |
| 5 | Flagged readings in red · loading / error / empty states | ✅ |
| 6 | CSS pass · `formatDepth()` from `shared.js` used on every number | ⬜ |

### P5 — Map Page *(beginner)*
| Day | Task | Status |
|---|---|---|
| 0–1 | JS + DOM basics · Leaflet map of India, 3 hardcoded markers (**CSS + JS tags**) | ✅ |
| 2 | Markers from `mock.json` · popup on click · coordinate bounds check | ⬜ |
| 3 | Switch to real API · 30 stations · click → `station.html?id=...` | ✅ |
| 4 | Colour dots by `status` (grey when null) · legend | ✅ |
| 5 | Station list beside the map, two-way highlight | ⬜ |
| 6 | Zoom, popup readability, small-window layout | ⬜ |

### P6 — Data + Testing + Demo *(beginner)*
| Day | Task | Status |
|---|---|---|
| 1 | **`data/stations.csv` — 30 real stations. Blocks P2 and P3. Finish today.** | ✅ |
| 2 | Validate readings: nulls, negatives, orphan station_ids | ✅ |
| 3 | Test all 5 endpoints at `/docs` · file issues with repro steps | ✅ |
| 4 | Check on-screen numbers vs API · hand-check one recharge · run the 5–25% rainfall check on all 30 | ⬜ |
| 5 | `docs/test-checklist.md` | ⬜ |
| 6 | Run the checklist · log every bug | ⬜ |
| 7 | Deploy frontend to Netlify with P2 | ⬜ |
| 8 | `README.md` (test it on a clean machine) · slide deck | ⬜ |
| 9 | **Demo the whole app solo** · record the backup video | ⬜ |

---

## Log

> Newest first. Format from `AGENTS.md` §7.

<!-- entries below -->

### [P6] Day 3 — Manual API Testing ✅ 2026-08-18
- Built: Manual verification of all 5 API endpoints via FastAPI `/docs`
- Learned: Interactive API documentation (Swagger UI) allows rapid testing of API contracts without writing frontend code
- Checked: All endpoints return expected formats, correct status codes (200, 404, 422), and handle edge cases gracefully
- Next: P6 Day 4 (Check on-screen numbers vs API, hand-check recharge, rainfall sanity check)

### [P6] Day 2 — Validated Generated Readings ✅ 2026-08-18
- Built: Fixed gap fault logic in `backend/validate_readings.py` Check 5
- Learned: "Gap" faults skip database insertion to simulate missing data, so they must be excluded from DB row counts
- Checked: All 5 validation checks passed (0 NULLs, 0 negative depths, 0 orphans, 0 out-of-range timestamps, 4333 exact fault matches)
- Next: P6 Day 3 (test all endpoints at /docs)

### [P3] Day 5 — Demo contrast tuning ✅ 2026-08-18
- Built: `DEMO_OVERRIDES` dict in `generate_data.py` — RJ-001 forced to +1.5 m/yr (steep decline), PB-002 forced to -0.5 m/yr (clear recovery)
- Learned: Overriding after the random roll preserves seed-42 state for all other stations
- Checked: RJ-001 computed +1.683 (Declining), PB-002 computed -0.317 (Recovering). All other 28 stations unchanged. Known limitation: HR-001 and KA-001 classify as Stable instead of Recovering due to +0.18 m/yr seasonal bias — documented, not an analytics bug.
- Next: P3 tasks complete. Support P6 validation and demo prep.

### [P3] Day 4 — Verified P1's trend against ground truth ✅ 2026-08-18
- Built: `backend/verify_trends.py` — independent verification of `calculate_trend()` and `get_status()`
- Learned: Replaying a fixed seed to recover ground-truth values; systematic bias from incomplete seasonal cycles
- Checked: `calculate_trend()` exact on synthetic data (5 slopes + 2 edge cases). `get_status()` correct on all 10 boundary cases. 28/30 station classifications match. 2 mismatches (HR-001, KA-001) caused by +0.18 m/yr seasonal bias in generator, not analytics bugs.
- Next: P3 Day 5 — tune demo contrast (one steeply declining, one recovering)

### [P4] Day 5 — Loading / error / empty states ✅ 2026-08-17
- Built: `chart-status` message element, `!response.ok` guard, `data.length === 0` guard, catch-block message
- Learned: Defensive programming — handling every path, not just the happy one
- Checked: Valid station loads chart; fake ID shows error; no ID shows missing message; server down shows connection error
- Next: Flagged readings in red (remaining P4 Day 5)

### [P5] Day 4 — Map colour dots + legend ✅ 2026-08-17
- Built: `getStatusColor()` switch helper, `L.circleMarker` replacing `L.marker`, legend in `index.html`
- Learned: Leaflet circleMarker, switch statements, conditional styling from API data
- Checked: All 30 stations render as coloured dots matching their precomputed status
- Next: Day 5 tasks

### [P4] Day 4 — Analytics Dashboard ✅ 2026-08-17
- Built: Frontend DOM updates in `station.html` and `station.js`
- Learned: Multiple asynchronous `fetch()` calls on a single page, manipulating `innerText`
- Checked: The station page now correctly displays the JSON data in the dashboard boxes
- Next: P5 Day 4 (Map styling)

### [P2] Day 4 — /analytics endpoint (Part 2) ✅ 2026-08-17
- Built: `GET /api/stations/{id}/analytics` endpoint in `backend/main.py`
- Learned: API Contracts, Presentation Layer logic, handling `NULL` database values
- Checked: Successfully returned structured JSON matching `04_API_CONTRACT.md`
- Next: P4 Day 4 (Frontend UI)

### [P2] Day 4 — refresh.py (Part 1) ✅ 2026-08-17
- Built: `backend/refresh.py` to precompute analytics for all stations
- Learned: Caching heavy math to DB instead of computing on request, explicit `INSERT` columns
- Checked: Successfully populated `trend_m_per_year`, `recharge_mm`, `anomaly_count`, and `status`
- Next: P2 Day 4 (Part 2: /analytics API endpoint)

### [P1] Day 4 — detect_anomalies() & get_status() ✅ 2026-08-16
- Built: `detect_anomalies()` and `get_status()` in `backend/analytics.py`
- Learned: Using index loops to compare adjacent elements, absolute differences for spikes
- Checked: Correctly catches anomalies and stuck sensors
- Next: P2 Day 4 (refresh.py)

### [P1] Day 3 — calculate_recharge() ✅ 2026-08-16
- Built: `calculate_recharge()` in `backend/analytics.py`
- Learned: Using max/min for Δh on m bgl data, Specific Yield formula
- Checked: Test block outputs exactly 168.0 mm
- Next: P1 Day 4 (detect_anomalies)

### [P1] Day 2 — calculate_trend() ✅ 2026-08-16
- Built: `calculate_trend()` in `backend/analytics.py`
- Learned: `np.polyfit` for linear regression, converting dates to elapsed days, scaling daily slope to yearly
- Checked: Test block outputs expected ~0.5 m/year trend
- Next: P1 Day 3 (calculate_recharge)

### [Day 3 Gate] Map → click station → real hydrograph ✅ 2026-08-16
- Built: `station.html`, Chart.js plotting, and the `/timeseries` FastAPI endpoint with `GROUP BY DATE`.
- Learned: `URLSearchParams`, Chart.js reversed y-axis, and SQL aggregations to prevent browser lag.
- Checked: The entire golden path works end-to-end.
- Next: P1 Analytics (`calculate_trend`, `calculate_recharge`)

### [P3] Day 2 — 3-year multi-station bulk generator ✅ 2026-08-16
- Built: `generate_data.py` logic to loop 30 stations and insert 131,400 rows
- Learned: `csv.reader`, indentation inside loops, tuple unpacking, and why `executemany` is essential for bulk inserts
- Checked: Script ran successfully without SQLite timeout/overhead
- Next: P3 Day 3 (Inject faults)

### [P3] Day 1 — single-station generator ✅ 2026-08-16
- Built: sine-wave based groundwater depth simulator
- Learned: math.sin for annual water cycles, timedelta loop mechanics, visual verification
- Checked: water table correctly rises (depth decreases) during monsoon
- Next: 3-year data generation with long-term trends

### [P6] Day 1 — stations.csv ✅ 2026-08-16
- Built: `data/stations.csv` with 30 real monitoring stations
- Learned: researching aquifer types, mapping real geology to simplified formations, Git commit and push
- Checked: CSV format, coordinates are valid, exact string matches for formations
- Next: P3 generate_data.py

### [P2] Day 1 — mock.json ✅ 2026-08-15
- Built: `frontend/mock.json` with 3 varied stations for UI testing
- Learned: decoupling frontend from backend, JSON formatting bugs, and interpreting water table depth
- Checked: JSON is valid
- Next: P6 stations.csv

### [P2] Day 1 — database.py built ✅ 2026-08-15
- Built: `backend/database.py` using plain `sqlite3`
- Learned: replacing SQLAlchemy with `sqlite3`, using raw SQL, `conn.commit()`
- Checked: script runs and creates `groundwater.db`
- Next: `mock.json` or `stations.csv`

---

## Blockers

| Since | Who | Blocked on | Needs | Status |
|---|---|---|---|---|
| | | | | |

> **45-minute rule:** stuck longer than that → post what you're trying, what you tried, and the exact error. On a 10-day project, a day of silent struggling is 10% of everything.

---

## Decisions

| Decision | Why | Rejected |
|---|---|---|
| Vanilla JS, no React | 3 beginners + 10 days; React costs 4 days before anything renders | React + Vite |
| Three JS files, not one shared `app.js` | No merge conflicts, and map code can't run on the station page | one `app.js` |
| SQLite with plain `sqlite3` | One file, no setup, they learn real SQL | Postgres, SQLAlchemy |
| Generated readings, fixed seed | WIMS is restricted; seed keeps numbers stable across DB rebuilds | scraping India-WRIS |
| Specific yield only in `analytics.py` | One source of truth; two copies would silently diverge | also in `stations.csv` |
| Status precomputed by `refresh.py` | 30 live analytics runs per page load would take seconds | compute on request |
| Water-year max−min for Δh | Works for both SW and NE monsoon regions | fixed May/October months |
| No ML / forecasting | Not needed for a working app; costs 3 days | SARIMA, LSTM |
| | | |

---

## Parking lot

Good ideas that are **not** in these 10 days. Write it here and move on.

| Idea | From |
|---|---|
| Forecasting the next 30 days | |
| District-level map colouring | |
| Mobile app | |
| Real India-WRIS integration | |
| Rainfall overlay to validate recharge | |
| Absolute-depth as well as rate in the status rule | |
| | |
