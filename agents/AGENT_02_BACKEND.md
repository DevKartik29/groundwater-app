# AGENT_02 — P2: Backend API + Database

> Read `AGENTS.md` first. **Skill level: comfortable with code, new to FastAPI/SQL.** Explain each new framework thing once, properly, then move fast.

## Mission
Data gets into a database and out through five endpoints. **Four people depend on your pipes.**

## You own
```
backend/database.py     create tables, connect, load stations.csv
backend/refresh.py      precompute each station's status (Day 4)
backend/main.py         the 5 endpoints
frontend/mock.json      hand-written, Day 1
requirements.txt
```

**Stack note: plain `sqlite3`, not SQLAlchemy.** You'll write real SQL. That's deliberate — in 10 days, learning an ORM's abstraction over SQL you don't yet know costs more than it saves, and SQL is the thing worth knowing.

---

## The single most important thing you do

**Day 1, before anything else: hand-write `frontend/mock.json`** with 3 fake stations in exactly the `/api/stations` shape.

P4 and P5 build against it from Day 1 and change one line on Day 3. Costs you 15 minutes. Saves three person-days of two beginners sitting idle waiting for your API.

---

## Day plan

| Day | Do |
|---|---|
| 1 | **`mock.json` first.** Then `database.py`: two tables + the index. |
| 2 | Load `stations.csv`, filling `specific_yield` from `analytics.SPECIFIC_YIELD`. `/api/health`, `/api/stations`. **Enable CORS today** — the frontend hits you tomorrow. Verify at `/docs`. |
| 3 | `/api/stations/{id}`, `/timeseries?days=365` (**daily averages via SQL `GROUP BY DATE(ts)`**, not raw 6-hourly). |
| 4 | `refresh.py` — run P1's functions once for all 30 stations and store `latest_level_m_bgl`, `trend_m_per_year`, `status`. Then `/api/stations/{id}/analytics`. |
| 5 | Add `flagged` to the timeseries response. Time each endpoint; anything over a second, check the index is being used. |
| 7 | Deploy to Render with P6 — read the warnings below first. |

---

## Four things to actually understand, not just copy

**1. The index.** `CREATE INDEX idx_readings_station_ts ON readings(station_id, ts)`. Without it, every request scans all 131,400 rows. With it, SQLite jumps straight to the right ones. Time the same query with and without — feeling the difference is worth more than being told about it.

**2. Daily aggregation.** A year of 6-hourly data is 1,460 points. Sending all of them makes the chart slow and unreadable. `GROUP BY DATE(ts)` collapses it to ~365 *in the database*, where it's cheap. Doing it in the browser means sending 4× the data to do the same job worse.

**3. Precompute vs compute-on-request.** `/api/stations` needs a status for all 30 stations. Computing live means running the analytics 30 times, over ~4,380 rows each, **on every page load** — several seconds per request. `refresh.py` computes it once and stores it, turning `/api/stations` into a single instant query. This trade-off is one of the most useful ideas in the whole project.
**Rule: whenever P3 regenerates data, re-run `refresh.py`.** Stale precomputed columns are the "why do the numbers look wrong?" bug.

**4. `specific_yield` is derived, not entered.** `stations.csv` has only `formation`. You fill the column at load time from `analytics.SPECIFIC_YIELD`. One source of truth — if the number lived in the CSV *and* the code they'd eventually disagree, and nobody would know which one the app used.

---

## Three sqlite3 gotchas that will cost you an hour each

**Threading:** FastAPI serves requests on multiple threads, and sqlite3 objects can't cross threads. Open with `check_same_thread=False`, and open a fresh connection per request rather than sharing one global. Otherwise: `SQLite objects created in a thread can only be used in that same thread`.

**Bulk inserts:** committing per row makes P3's 131,400-row insert take minutes. Build a list of tuples, one `cur.executemany(...)`, one `conn.commit()`. Seconds instead of minutes.

**Database path:** a relative path like `"groundwater.db"` resolves from wherever the command was *run*, so running from different folders silently creates *different* databases. Build one absolute path from `__file__` and everyone stops losing time to this.

---

## ⚠️ Day 7: Render's free tier will delete your database

Three facts you must plan around:

1. **The filesystem is ephemeral.** Your SQLite file is deleted on every redeploy, restart, and spin-down. Free services cannot attach a persistent disk. **Fix:** rebuild the DB in the start command —
   `python -m backend.database && python -m backend.generate_data && python -m backend.refresh && uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   This is exactly why P3 uses a fixed random seed: the rebuilt database must contain the same numbers you tested.
2. **Free services spin down after 15 minutes of no traffic** and take ~1 minute to wake. On demo day, open the site 5 minutes before presenting.
3. **Bind to `0.0.0.0` and `$PORT`.** Render sets `$PORT`; ignoring it gives you a 502.

Also update `allow_origins` to the real Netlify URL, and keep the localhost ones for local development.

---

## Traps

| Trap | Instead |
|---|---|
| Building the API before the mock | Mock first, Day 1 |
| `SELECT *` then filtering in Python | Filter in SQL. Always. |
| Forgetting CORS | Day 2. The browser silently refuses to load your data and P4 loses an afternoon. Include **both** `127.0.0.1:5500` and `localhost:5500` — they're different origins. |
| Returning raw 6-hourly points | Daily averages |
| String-formatting values into SQL | Use `?` placeholders — safer and less fiddly |
| Forgetting to re-run `refresh.py` after data changes | Make it the last line of whatever regenerates data |
| Deploying on Day 9 | Day 7 |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_02_BACKEND.md, 04_API_CONTRACT.md, and PROGRESS.md.
Two sentences: what day, what's next. One question. No code yet.
```

**Database (Day 1):**
```
Day 1: backend/database.py with plain sqlite3.
Before code, explain in 3 sentences each: primary key, foreign key, and what an
index actually does to a query. Use our stations/readings tables as the example.
Then show me the CREATE TABLE statements only. Then stop.
```

**An endpoint:**
```
Build GET /api/stations/{id}/timeseries exactly per 04_API_CONTRACT.md §4.
Requirements: daily averages via SQL GROUP BY (not in Python), ? placeholders,
404 if the station doesn't exist, empty list (not 404) if there are no readings,
no SELECT *.
Show me the SQL query first and explain what GROUP BY is doing. Then give me
just the route signature — I'll write the body.
```

**refresh.py (Day 4):**
```
Day 4: backend/refresh.py.
Before code, explain the trade-off between computing a value on every request
versus computing it once and storing it. Which does our /api/stations need, and why?
Then show me the loop structure only — I'll write the update statement.
```

**Debugging:**
```
This endpoint returns 500: [paste the full traceback from the uvicorn terminal]
Do NOT fix it. First: what does this traceback say, line by line? Three most
likely causes, ranked? What do I check first? Then wait.
```

**CORS (you will hit this):**
```
My frontend gets a CORS error. Explain what CORS actually is and why the browser
blocks this — not just the fix. Then show me the FastAPI middleware config,
and tell me why 127.0.0.1 and localhost count as different origins.
```

## Learning (chat, not IDE)
```
Explain what a database index actually is — the data structure, not the metaphor.
Then explain why INDEX(station_id, ts) helps the query "one station's last 365
days" but an index on ts alone wouldn't. Quiz me after.
```
