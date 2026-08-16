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
| 3 | **Map → click station → real hydrograph.** The whole path works. | ⬜ |
| 4 | `refresh.py` run · map dots coloured · station page shows trend, recharge, anomalies | ⬜ |
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
| 2 | `calculate_trend()` + test on a series with a known slope (check the ×365.25) | ⬜ |
| 3 | `calculate_recharge()` + test (Δh 1.2 m × Sy 0.14 → 168 mm) | ⬜ |
| 4 | `detect_anomalies()` + `get_status()`, checked against P3's broken rows | ⬜ |
| 5 | Review everything · hunt the depth-vs-elevation bug · verify numbers by hand | ⬜ |
| 6 | Empty and error states across the app | ⬜ |
| 8 | `docs/methodology.md` | ⬜ |
| — | **Daily:** PR reviews within hours · run the evening merge · keep this file true | ⬜ |

### P2 — Backend API + Database
| Day | Task | Status |
|---|---|---|
| 1 | **`mock.json` first** · `database.py` (2 tables + index) | ✅ |
| 2 | Load `stations.csv`, fill `specific_yield` from P1's dict · `/api/health` · `/api/stations` · **CORS** | ⬜ |
| 3 | `/api/stations/{id}` · `/timeseries` (daily averages via SQL) | ⬜ |
| 4 | `refresh.py` (precompute status) · `/analytics` endpoint | ⬜ |
| 5 | `flagged` in timeseries response · time every endpoint | ⬜ |
| 7 | Deploy to Render — **rebuild DB in the start command** | ⬜ |

### P3 — Data Generator
| Day | Task | Status |
|---|---|---|
| 1 | One station, one year, 6-hourly. **Plot it and look at it.** | ✅ |
| 2 | 30 stations × 3 years = 131,400 readings · **fixed random seed** · `executemany` | ✅ |
| 3 | Inject faults (stuck, spike, gap) · **keep the list of broken rows** · leave flags as OK | ⬜ |
| 4 | **Verify P1's trend against the decline you built in** — you're the only one with ground truth | ⬜ |
| 5 | Tune for demo contrast: one steeply declining, one recovering | ⬜ |

### P4 — Station Page + Charts *(beginner)*
| Day | Task | Status |
|---|---|---|
| 0–1 | JS + DOM basics · page that `fetch`es `mock.json` and prints names | ⬜ |
| 2 | `station.html` + Chart.js line chart, **y-axis reversed** (P1 verifies) | ⬜ |
| 3 | Switch to real API · read station id via `URLSearchParams` · real data | ⬜ |
| 4 | Show trend, recharge, latest reading, anomaly count | ⬜ |
| 5 | Flagged readings in red · loading / error / empty states | ⬜ |
| 6 | CSS pass · `formatDepth()` from `shared.js` used on every number | ⬜ |

### P5 — Map Page *(beginner)*
| Day | Task | Status |
|---|---|---|
| 0–1 | JS + DOM basics · Leaflet map of India, 3 hardcoded markers (**CSS + JS tags**) | ⬜ |
| 2 | Markers from `mock.json` · popup on click · coordinate bounds check | ⬜ |
| 3 | Switch to real API · 30 stations · click → `station.html?id=...` | ⬜ |
| 4 | Colour dots by `status` (grey when null) · legend | ⬜ |
| 5 | Station list beside the map, two-way highlight | ⬜ |
| 6 | Zoom, popup readability, small-window layout | ⬜ |

### P6 — Data + Testing + Demo *(beginner)*
| Day | Task | Status |
|---|---|---|
| 1 | **`data/stations.csv` — 30 real stations. Blocks P2 and P3. Finish today.** | ✅ |
| 2 | Validate readings: nulls, negatives, orphan station_ids | ⬜ |
| 3 | Test all 5 endpoints at `/docs` · file issues with repro steps | ⬜ |
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
