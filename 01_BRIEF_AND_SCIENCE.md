# 01 — What We're Building (and the minimum science)

**Project:** Real-Time Groundwater Resource Evaluation Using DWLR Data (SIH25068, Ministry of Jal Shakti)
**Time:** 10 days · **Team:** 6 · **Goal:** a small app that works, that all six of us understand.

---

## 1. The problem in three sentences

CGWB monitors India's groundwater with ~25,000 wells measured **4 times a year** — useless for spotting a problem early. They're installing **5,260 DWLRs** (Digital Water Level Recorders) that log water level automatically **every 6 hours**. The ask: turn that stream into something a planner can look at and act on.

## 2. What we build (and nothing more)

**One web app with two screens.**

**Screen 1 — Map.** 30 monitoring stations across India as coloured dots. Green = fine, yellow = watch, red = declining. Click a dot → screen 2.

**Screen 2 — Station detail.** For one station:
- A **hydrograph** (water level over the last year)
- **Latest reading** in metres below ground
- **Trend**: falling/rising at X metres per year
- **Recharge**: estimated mm added during the last water year
- **Data health**: how many readings were flagged as bad sensor data

That's the whole product. Five numbers and two screens.

### Explicitly NOT building
No login. No mobile app. No machine learning or forecasting. No district-level aggregation. No alerts page. No live scraping of government portals. If someone suggests one of these, write it in `PROGRESS.md` under Parking Lot and move on.

---

## 3. Stack — locked, do not change

| Layer | What | Why this |
|---|---|---|
| Backend | **Python + FastAPI** | Analytics needs Python. FastAPI gives free API docs at `/docs`. |
| Database | **SQLite + plain `sqlite3`** | One file, zero setup, no ORM to learn. You write real SQL — that's the point. |
| Data | **A Python script that generates realistic readings** | See §5. |
| Frontend | **Plain HTML + CSS + JavaScript** | **No React, no npm, no build step.** |
| Charts | **Chart.js** from a CDN | One `<script>` tag. |
| Map | **Leaflet** from a CDN | One `<script>` tag + **one `<link>` for its CSS**. Free, no API key. |
| Version control | Git + GitHub | |
| IDE | Antigravity + Gemini Pro | Rules in `AGENTS.md` |

**Why no React:** with three complete beginners and ten days, React costs you four days of learning (JSX, props, state, hooks, npm, Vite, `node_modules`) before anyone renders a chart. Vanilla JS gets them to `fetch()` → update the page on day two. You will learn the *actual* workflow — HTTP request, JSON response, DOM update — more clearly without a framework in the way.

---

## 4. Architecture — the whole thing

```
   generate_data.py  ──►  groundwater.db  ──►  main.py     ──►  browser
   (makes realistic       (SQLite file:        (FastAPI,        (2 HTML pages
    readings)              stations,            5 endpoints)     + Chart.js
                           readings)                             + Leaflet)
                               ▲    ▲
                    refresh.py │    │ analytics.py
              (precomputes status)  (trend · recharge · anomalies)
```

Five Python files, six frontend files, one database.

```
groundwater-app/
├── AGENTS.md
├── PROGRESS.md
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── stations.csv         ← P6
├── docs/
│   ├── methodology.md       ← P1 (Day 8)
│   ├── test-checklist.md    ← P6 (Day 5)
│   └── team/                ← everyone (Git exercise)
├── backend/
│   ├── __init__.py          ← empty file, makes `backend` importable
│   ├── database.py          ← P2: create tables, connect, load stations.csv
│   ├── generate_data.py     ← P3: fill the DB with readings
│   ├── analytics.py         ← P1: trend, recharge, anomalies, Sy lookup
│   ├── refresh.py           ← P2: precompute each station's status (Day 4)
│   └── main.py              ← P2: the 5 API endpoints
└── frontend/
    ├── index.html           ← P5: the map page
    ├── station.html         ← P4: the detail page
    ├── style.css            ← P4
    ├── shared.js            ← P1: API base URL + shared helpers
    ├── map.js               ← P5
    └── station.js           ← P4
```

> **Three JS files, not one.** `map.js` loads only on `index.html`, `station.js` only on `station.html`. This means P4 and P5 never edit the same file (no merge conflicts) **and** map code never runs on the station page (which would throw "map container not found" errors on a page with no map). One shared file would have caused both problems.

---

## 5. Where the data comes from — read this, it matters

The live 6-hourly DWLR feed sits behind **WIMS**, which is restricted to authorised government agencies. **You will not get access in 10 days.** India-WRIS publishes some data publicly but through an unstable, undocumented interface.

**So:** P6 collects **real station details** (real names, real districts, real coordinates, real formations) from CGWB's public pages, and P3 writes a script that generates **realistic readings** for those stations.

This is not cheating, and you should say it out loud: *"Live telemetry is restricted to authorised agencies. Our app reads from a database — plug in the real feed and nothing else changes."* That's true, and it's the honest engineering answer.

**Scale:** 30 stations × 3 years × 4 readings/day = **131,400 readings** (4,380 per station). Small enough for SQLite, big enough that a missing database index is noticeable — which is a useful thing to feel for yourself.

---

## 6. The minimum groundwater science — everyone reads this

Five things. Twenty-five minutes. Nobody skips this.

### (a) Water level means DEPTH BELOW GROUND
Readings are **metres below ground level (m bgl)**.

> **A BIGGER number means the water is DEEPER, which is WORSE.**
> The number going **up** means the water table is going **down**.

This is backwards from everyone's intuition and it is the #1 bug in projects like this.

**Two rules that prevent it:**
1. Always name the variable `water_level_m_bgl`. Never `level`.
2. **Every chart's y-axis is reversed** — small numbers (shallow) at the top. In Chart.js: `y: { reverse: true }`. P4 sets this on Day 2 and P1 verifies it.

### (b) Specific yield (Sy) turns metres into millimetres of water
Rock isn't a bucket — water sits in the gaps between grains. **Specific yield** is the fraction that actually drains. A 1 m rise in an aquifer with Sy = 0.10 means 100 mm of water arrived.

| `formation` (exact spelling) | Sy |
|---|---|
| `alluvium_sandy` | 0.14 |
| `alluvium_silty` | 0.08 |
| `sandstone` | 0.05 |
| `weathered_granite` | 0.025 |
| `basalt` | 0.015 |

> **Single source of truth:** this table lives in **`backend/analytics.py` only**, as a dictionary. `stations.csv` carries the `formation` name, *not* the number. If the value existed in two places they would eventually disagree, and nobody would notice which one the app was actually using.

### (c) Recharge = Δh × Sy
The water table rises during the monsoon. That rise, times specific yield, is the recharge.

**How we pick Δh — the water-year method:**
A **water year** runs **1 June to 31 May** (it starts just before the monsoon, so one monsoon sits inside one water year).

```
Δh              = (deepest level in the water year) − (shallowest level in the water year)
recharge in mm  = Δh × Sy × 1000
```

> Why max−min over a water year instead of "May level minus October level"? Because monsoon timing differs across India — Tamil Nadu gets the **north-east** monsoon in October–December, not the south-west monsoon in June–September. Fixed month windows would produce nonsense for our Tamil Nadu stations. Max−min within a water year works for both.

**Worked example (our demo station):**
Ludhiana, Punjab. `alluvium_sandy`, Sy = 0.14. Over water year 2025–26 the level ranged from 25.4 m bgl (deepest, pre-monsoon) to 24.2 m bgl (shallowest, post-monsoon).
Δh = 25.4 − 24.2 = **1.2 m** → recharge = 1.2 × 0.14 × 1000 = **168 mm**.

**Sanity check:** recharge is usually **5–25% of annual rainfall**. Ludhiana gets roughly 700–750 mm a year, so 168 mm is about **23%** — high but plausible for sandy alluvium. If your number comes out at 500 mm, you have a bug. **Run this check on every station.**

### (d) Trend = how fast it's falling, per year
Fit a straight line through the daily average levels. The slope is **metres per year**.

> **Units trap:** if your x-axis is *days since the first reading*, `numpy.polyfit` gives you metres **per day**. Multiply by **365.25** to get metres per year. Forgetting this gives you a number ~365× too small, which looks like "no trend" and is very easy to miss. P3 can catch it on Day 4 (see §e of their file).

- Slope **positive** (depth increasing) → water table **falling** → 🔴 bad
- Slope **negative** → water table **rising** → 🟢 good

Our status rules:
| Status | Rule | Colour |
|---|---|---|
| `safe` | falling slower than 0.1 m/yr, or rising | 🟢 green |
| `watch` | falling 0.1 – 0.3 m/yr | 🟡 yellow |
| `critical` | falling faster than 0.3 m/yr | 🔴 red |

> **Known simplification, say it if asked:** we classify on *rate of change* only, not absolute depth. A station sitting stably at 40 m comes out `safe` even though it's deep. Real CGWB assessment also weighs extraction against recharge; we don't have extraction data. Knowing your own simplification and naming it is better than being caught by it.

### (e) Sensors lie — this is our best feature
Real DWLRs fail. Detect two kinds:
- **Stuck sensor** — the exact same value 12+ times in a row (12 readings = 3 days). Real water levels always wobble slightly, so an exactly-repeating value means the sensor has frozen.
- **Spike** — one reading metres away from its neighbours, then back to normal.

**Never delete a bad reading.** Mark it with a `quality_flag` and show it differently on the chart. Anyone can plot a line; showing that you know when the sensor itself is wrong is what impresses people who work with this data.

---

## 7. Six questions everyone must answer before Day 3

Post your answers in the team channel. P1 checks them.

1. A station reads 8.2 m bgl in 2024 and 11.6 m bgl in 2026. Better or worse? By how much did the water table move, and at what rate per year?
2. Why is the chart's y-axis reversed?
3. Δh is 2.0 m at a basalt station (Sy = 0.015). What's the recharge in mm?
4. A sensor reports 6.4400 exactly, 30 times in a row. What's wrong, and what do we do with those rows?
5. Where does our reading data come from, and what do we say when someone asks if it's real?
6. `calculate_trend()` returns 0.0017. What's probably wrong? (Hint: §6d.)

**Answers to check against:** 1 — worse; the water table fell 3.4 m in 2 years, ≈1.7 m/yr. 2 — because depth increases downward, so reversing it makes the line move the same direction as the actual water table. 3 — 2.0 × 0.015 × 1000 = 30 mm. 4 — stuck sensor; flag those rows `STUCK`, keep them, exclude them from trend and recharge maths, show them in red on the chart. 5 — generated by us for real CGWB station locations, because live telemetry is behind restricted WIMS access; the app reads a database, so the real feed drops straight in. 6 — the slope is still in metres per **day**; multiply by 365.25.
