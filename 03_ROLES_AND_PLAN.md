# 03 — Roles & the 10-Day Plan

---

## The six roles

| | Name | Role | Owns | Level |
|---|---|---|---|---|
| **P1** | ______ (you) | Lead + Analytics | `backend/analytics.py`, `frontend/shared.js`, all PR reviews, integration | comfortable |
| **P2** | ______ | Backend API + Database | `backend/database.py`, `main.py`, `refresh.py` | comfortable |
| **P3** | ______ | Data Generator + Sensor Faults | `backend/generate_data.py` | comfortable |
| **P4** | ______ | Station Page + Charts | `frontend/station.html`, `station.js`, `style.css` | beginner |
| **P5** | ______ | Map Page | `frontend/index.html`, `map.js` | beginner |
| **P6** | ______ | Station Data + Testing + Demo | `data/stations.csv`, `README.md`, `docs/`, the deck | beginner |

**One rule prevents almost all merge conflicts: you edit files in your own row.** To change someone else's file, message them first.

**Nobody shares a source file.** P4 and P5 each have their own JS file; the only shared one is `shared.js`, which P1 owns and which should barely change after Day 1. This is deliberate — on a 10-day project you cannot afford an afternoon lost to a merge conflict.

---

## Why the split works

The three hard, uncertain pieces — the maths, the API, and the data generator — go to the three who can move without hand-holding. Uncertainty is expensive; put it where it costs least.

The three beginner roles are each: **visually verifiable** (you see instantly whether it works), **well-bounded** (one file, one screen), and **not blocking anyone in the first three days**.

**P6's role is not the leftover job.** In ten days the two things that actually decide whether this works are: does the demo run, and can you explain it. P6 owns both — and owns `stations.csv`, which blocks everybody until it exists.

---

## The dependency chain

```
Day 1   P6: stations.csv  ──────────►  blocks P2 and P3
Day 1   P1: analytics.py Sy lookup ─►  P2 needs it to fill the DB
Day 2   P2: database + tables  ──────►  P3 fills it with readings
Day 2   P2: /api/stations  ──────────►  P4 and P5 can fetch real data on Day 3
Day 4   P1: analytics functions  ────►  P2's refresh.py + /analytics endpoint
```

**The trap:** P4 and P5 idle for three days waiting for the API.

**The fix — Day 1.** P2 hand-writes `frontend/mock.json`: 3 fake stations in exactly the shape `04_API_CONTRACT.md` describes. P4 and P5 build against that file from Day 1 and switch one line on Day 3. **Nobody is ever blocked.** Fifteen minutes of P2's time, three person-days saved.

---

# The 10-day plan

Each day ends with **everything merged to `main` and the app still running.** Not "mostly working on my branch" — merged.

---

### DAY 0 — Setup *(everyone, ~3 hours)*
- Install checklist (`02_SETUP.md`) — post your version output
- Read `01_BRIEF_AND_SCIENCE.md`, answer the six questions
- Read `05_GIT_QUICKSTART.md`, do the exercise: branch → commit → push → PR → merged
- P1 creates the repo with `.gitignore`, `AGENTS.md`, `PROGRESS.md`, the folder skeleton, and `backend/__init__.py`

**Nobody writes app code today.** It feels wasted. It isn't — this is the day that stops someone still fighting `pip` on Day 6.

---

### DAY 1 — Foundations
| | |
|---|---|
| **P1** | Write `04_API_CONTRACT.md` — exact endpoints and JSON shapes — and send it to everyone. Write `analytics.py` function signatures + docstrings (no bodies) **and the `SPECIFIC_YIELD` dictionary**, which P2 needs tomorrow. Write `frontend/shared.js` (the `API` constant, `fetchJSON`, `formatDepth`). |
| **P2** | `database.py`: create the two tables + the index. **First job of the day: hand-write `frontend/mock.json` and give it to P4/P5.** |
| **P3** | Start `generate_data.py`: one station, one year of 6-hourly readings with a monsoon rise and dry-season fall. **Plot it and look at it.** Does it resemble a real hydrograph? |
| **P4** | JS + DOM learning. Then a plain HTML page that reads `mock.json` with `fetch()` and prints station names. |
| **P5** | JS + DOM learning. Then a Leaflet map centred on India with 3 hardcoded markers. |
| **P6** | **`data/stations.csv` — 30 real CGWB stations.** Blocks P2 and P3, so finish it today. Columns: `station_id, name, state, district, lat, lon, formation`. |

> **P6:** pick contrasting places — Punjab (alluvium, badly over-pumped), Rajasthan (hard rock, deep), Maharashtra (basalt), Tamil Nadu, West Bengal. Different formations mean different specific yields, which makes the demo mean something.
> **Check every coordinate: India is latitude 6–37, longitude 68–98.** One typo and a station lands in the ocean.
> **`formation` must be spelled exactly as in the science doc** (`alluvium_sandy`, not `Alluvium Sandy`) — P1's lookup matches on that exact string, and a typo silently produces a wrong recharge number.

**End of day:** stations.csv exists · mock.json exists · a map renders · a page prints names.

---

### DAY 2 — Data in the database
| | |
|---|---|
| **P1** | `calculate_trend()` — fit a line to daily averages, return **metres per year** (remember the ×365.25). Test on made-up data where you know the answer. |
| **P2** | Load `stations.csv` into the `stations` table, filling `specific_yield` from P1's lookup. Write `GET /api/health` and `GET /api/stations`. **Enable CORS today** — the frontend hits you tomorrow. Check both at `/docs`. |
| **P3** | Generator for all 30 stations: **3 years of 6-hourly data** (4,380 readings each, 131,400 total), monsoon cycle + a per-station long-term decline. **Use a fixed random seed** — see the note below. Insert into the DB. |
| **P4** | `station.html` skeleton + a **Chart.js line chart with `reverse: true` on the y-axis**, drawing hardcoded data. |
| **P5** | Map reads markers from `mock.json`. Click a marker → popup with the station name. Add the coordinate bounds check. |
| **P6** | Validate the readings: nulls? negative depths? any `station_id` in `readings` that isn't in `stations`? Report what you find. |

> **Fixed random seed (`random.seed(42)` / `np.random.default_rng(42)`) — do this, it matters twice.** First, whenever the database is rebuilt the numbers stay identical, so P6's screenshots and the slide deck don't go stale. Second, when the app is deployed the database gets rebuilt on the server (see Day 7) — without a seed, the live app would show different numbers from the one you tested.

**End of day:** the database holds 30 stations and 131,400 readings. `/api/stations` returns real JSON.

---

### DAY 3 — First real connection *(the day it becomes a real app)*
| | |
|---|---|
| **P1** | `calculate_recharge()` — water-year max−min × Sy × 1000. Test against the worked example (Δh 1.2 m, Sy 0.14 → 168 mm). |
| **P2** | `GET /api/stations/{id}` and `GET /api/stations/{id}/timeseries?days=365`. **Return daily averages via SQL `GROUP BY DATE(ts)`, not raw 6-hourly points** — a year of raw data is 1,460 points and will make the chart sluggish. |
| **P3** | Add sensor faults to the generator: stuck values, spikes, gaps. **Keep the list of rows you broke** — it's P1's test set. Leave `quality_flag` as `'OK'`; the detector has to find them unaided. |
| **P4** | **Switch from `mock.json` to the real API** (one line in `shared.js`). Chart draws real data. Read the station id from the URL with `URLSearchParams`. |
| **P5** | **Switch to the real API.** All 30 stations on the map. Click → opens `station.html?id=...` |
| **P6** | Test every endpoint at `/docs`. File anything broken as a GitHub issue with steps to reproduce. |

**End-of-day gate:** open the map → click a station → see its real hydrograph.
**If this doesn't work by end of Day 3, stop adding features and fix it.** Everything after this is decoration on top of this one working path.

---

### DAY 4 — Analytics
| | |
|---|---|
| **P1** | `detect_anomalies()` — stuck (12+ identical) and spike (far from the local median). Test against P3's list of broken rows. Then `get_status()` → safe/watch/critical. |
| **P2** | `refresh.py`: run P1's functions for all 30 stations once and **store** `latest_level_m_bgl`, `trend_m_per_year`, `status` in the `stations` table. Then `/api/stations` is a single fast query. Add `GET /api/stations/{id}/analytics`. |
| **P3** | **Verify P1's numbers against your ground truth.** You built a 0.6 m/yr decline into PB-001 — does `calculate_trend()` return ≈0.6? If it says 0.0016, that's the ×365.25 bug. **You are the only person who can run this check.** |
| **P4** | Station page shows trend, recharge, latest reading, anomaly count. Real numbers, real units. |
| **P5** | Colour map dots by `status`. Add a legend. |
| **P6** | Check every number on screen against the API response. Hand-calculate one station's recharge and compare. Run the 5–25%-of-rainfall sanity check on all 30. |

> **Why `refresh.py` instead of computing on request:** `/api/stations` needs a status for all 30 stations. Computing that live means running the analytics 30 times, over ~4,380 rows each, on *every single page load* — several seconds per request. Precomputing once and storing the answer turns it into one instant query. This trade-off (compute once and store vs. compute every time) is one of the most useful ideas in the whole project. Re-run `refresh.py` whenever the data changes.

---

### DAY 5 — Complete the loop
| | |
|---|---|
| **P1** | Review everything. Grep specifically for the depth-vs-elevation bug. Verify every displayed number by hand. Confirm P4's y-axis is reversed. |
| **P2** | Mark bad readings in the timeseries response so the chart can show them. Time each endpoint; anything over a second, check the index is being used. |
| **P3** | Tune the data for demo contrast: one clearly over-exploited station (steep decline), one recovering station (rising water table). Judges remember contrast. |
| **P4** | Flagged readings shown in red · loading, error and empty states |
| **P5** | Station list beside the map; clicking either one highlights the other |
| **P6** | Write `docs/test-checklist.md` — every screen, every click path, every state |

**End of day: the app is feature-complete. Feature freeze.** Anyone adding a new feature after today gets reverted.

---

### DAY 6 — Make it not ugly, make it not break
| | |
|---|---|
| **All** | Bug bash. P6 runs the checklist; everyone fixes what's found in their own files. |
| **P4** | Real CSS pass. Consistent fonts, spacing, colours. `formatDepth()` from `shared.js` used on **every** number. |
| **P5** | Map polish: sensible zoom, readable popups, works in a small window. |
| **P1** | Every empty and error state: what happens when a station has too little data? When the API is down? |

---

### DAY 7 — Deploy
| | |
|---|---|
| **P2 + P6** | Backend → **Render** (free). Frontend → **Netlify** (drag the `frontend` folder in). Change `API` in `shared.js` to the Render URL and update the CORS origins. |
| **Everyone else** | Test the live URL from your own phone and laptop. Report anything broken. |

> **Three things about Render's free tier that will bite you if you don't plan for them:**
>
> **1. The filesystem is ephemeral.** Your `groundwater.db` file is **deleted every time the service redeploys, restarts, or spins down.** Free services cannot attach a persistent disk. **Fix:** make the start command build the database first, e.g.
> `python -m backend.database && python -m backend.generate_data && python -m backend.refresh && uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
> This is exactly why the fixed random seed matters — the rebuilt database must contain the same numbers you tested.
>
> **2. Free services spin down after 15 minutes with no traffic**, and take about a minute to wake up. **On demo day, open the site 5 minutes before you present** so it's already awake. Otherwise your first click is a 60-second blank screen in front of the judges.
>
> **3. Mixed content.** Netlify serves over **https**; if `API` still points at `http://127.0.0.1:8000`, the browser blocks the request entirely. Both must be https, or both local. Don't half-deploy.

> Budget the whole day. **If it's not deployed by end of Day 7, stop and demo locally** — a working local demo beats a broken live one every time.

---

### DAY 8 — Documentation & story
| | |
|---|---|
| **P6** | `README.md` — then follow your own instructions on a clean machine. They'll be wrong. Fix them. Build the slide deck. |
| **P1** | `docs/methodology.md`: where each number comes from, which formula, what assumptions, what the uncertainty is. **This is your answer script when someone asks how you got that recharge figure.** |
| **P2/P3/P4/P5** | Each write 5 lines about your part for the README. Then read someone else's and check you understand it. |

---

### DAY 9 — Rehearsal
- **Full dry run, timed, twice.** Someone outside the team watches.
- **P6 demos the whole thing alone.** If the person who didn't write the backend can run the demo unaided, the product works.
- Every person answers: *"explain your part in 2 minutes, without notes."*
- Record a **3-minute backup video**. Venue wifi fails; assume it will.
- Prepare answers to the four questions you *will* be asked: *Is this real data? How did you calculate recharge? How accurate is it? What happens with 5,260 stations instead of 30?*

---

### DAY 10 — Buffer
Do not schedule work here. Something will have slipped, and this is where it goes. If nothing slipped, rehearse again and rest.

---

## Daily rhythm

- **Morning, 10 min:** everyone posts *doing today / blocked on*
- **Evening, 20 min:** everyone merges to `main`, and the app runs end to end
- **Stuck for 45 minutes?** Post it: what you're trying, what you tried, the exact error. Silent struggling is the single biggest cause of blown deadlines on student teams. Nobody is judged for asking at 45 minutes; everyone is judged for surfacing a blocker on day four of ten.
