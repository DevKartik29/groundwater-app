# AGENT_03 — P3: Data Generator + Sensor Faults

> Read `AGENTS.md` first. **Skill level: comfortable with code.** Explain the time-series ideas carefully — they're less obvious than they look — then move fast.

## Mission
There is no live data. **You make the data the entire app runs on.**

If your readings look fake, the whole demo looks fake. If they look like a real hydrograph, everything downstream is convincing.

## You own
```
backend/generate_data.py
```

## Why this is real work, not a shortcut
The live 6-hourly DWLR feed sits behind **WIMS**, restricted to authorised government agencies. You will not get access in 10 days. Every team facing this either fakes it badly and hides it, or builds a proper generator and says so. **We say so** — and the sentence that makes it fine is: *"the app reads from a database; plug in the real feed and nothing else changes."*

That's true, and it's why P2's design matters as much as yours.

---

## What a realistic hydrograph contains

Build these four layers and add them together:

1. **A baseline depth** — different per station (Punjab alluvium ~24 m, a shallow Bengal station ~5 m)
2. **The monsoon cycle** — water table rises sharply June–September (depth *decreases*), then recedes slowly through the dry season. **Not a sine wave: sharp rise, slow fall.** For Tamil Nadu stations shift the rise to October–December (north-east monsoon) — it takes one line and it makes the map genuinely more credible.
3. **A long-term trend** — a slow decline over the 3 years, different per station. This is what P1's `calculate_trend()` must find.
4. **Noise** — small random wobble, ~1–3 cm. Real sensors are never perfectly smooth, and this matters more than you'd expect: without it, "stuck sensor" has nothing to be distinguishable from.

> **Watch the sign.** Levels are *depth below ground*. Monsoon recharge makes the number **smaller**. A declining water table makes it **bigger**. Get this backwards and the chart looks fine while saying the opposite of the truth.

---

## Three technical requirements

**Fixed random seed — `np.random.default_rng(42)` or `random.seed(42)`.** This matters twice over. First, whenever the database is rebuilt the numbers stay identical, so P6's screenshots and the slide deck don't go stale. Second, the **deployed** app rebuilds the database on the server on every restart (Render's free filesystem is ephemeral) — without a seed, the live app would show different numbers from the one you tested. **This is not optional.**

**Bulk insert.** 131,400 rows committed one at a time takes minutes. Build a list of tuples, use one `cur.executemany(...)`, then one `conn.commit()`. Seconds instead of minutes.

**Volume.** 30 stations × 3 years × 4 readings/day = **4,380 per station, 131,400 total.** Three years, not two — a trend fitted over two years is thin, and P1's `insufficient_data` guard needs something to comfortably clear.

---

## Day plan

| Day | Do |
|---|---|
| 1 | One station, one year, 6-hourly. **Plot it and look at it.** Does it look like a real hydrograph? |
| 2 | All 30 stations, 3 years, per-station baseline and decline rate. Fixed seed. `executemany`. Insert into the DB. |
| 3 | Inject faults: stuck, spikes, gaps. **Save the list of rows you broke.** |
| 4 | **Verify P1's computed trend against the trend you built in.** |
| 5 | Tune for demo contrast: one clearly over-exploited station, one recovering |

---

## Day 4 is your highest-value hour

**You know the true answer because you created it.** Nobody else on the team can run this check.

If you built a 0.6 m/yr decline into PB-001 and `calculate_trend()` returns ≈0.6 — the analytics are right.
If it returns **0.0016**, that's the units bug: the slope is still in metres per *day* and needs ×365.25.
If it returns **−0.6**, the sign is flipped somewhere.
If it returns something wild like 8.0, a spike you injected isn't being excluded from the fit.

Each of those mismatches has a distinct signature. Learn to read them.

Same on Day 3: the list of rows you deliberately broke is the test set for P1's anomaly detector. Precision and recall against a known answer, on day 4 of a 10-day project, is a genuinely strong position — and one line in the pitch.

---

## The three faults to inject

| Fault | How | Why it's realistic |
|---|---|---|
| **Stuck** | Repeat one exact value 20–40 times | The sensor freezes; the number stops moving entirely |
| **Spike** | One reading several metres off, then back | Electrical glitch in the transducer |
| **Gap** | Delete a run of rows | Telemetry drops out, battery dies |

**Leave `quality_flag` as `'OK'` in the database.** P1's detector has to find them unaided. Pre-labelling them means you've tested nothing.

Aim for roughly **1% of readings** faulty — enough to be visible on the chart, not so much it looks broken.

---

## Traps

| Trap | Instead |
|---|---|
| Data that's too clean | Real sensors wobble. No noise means "stuck" detection has nothing to detect. |
| A pure sine wave | Sharp monsoon rise, slow recession. A sine wave looks wrong to anyone who's seen a real hydrograph. |
| Every station identical | Different baselines, decline rates, formations, monsoon timing. Contrast is what makes the demo land. |
| No random seed | The deployed app shows different numbers from the one you tested |
| Pre-labelling injected faults | Then P1's detector is untested |
| Generating 30 stations before checking 1 | Plot one. Look at it. Then scale. |
| Committing per row | `executemany` + one commit |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_03_DATA.md, 01_BRIEF_AND_SCIENCE.md §6, and PROGRESS.md.
Two sentences: what day, what's next. One question. No code yet.
```

**Day 1:**
```
Day 1: generate realistic 6-hourly groundwater readings for one station.
Before code, break a real Indian hydrograph into its parts: baseline depth,
monsoon cycle shape, long-term trend, noise. For each, tell me realistic
magnitudes and — importantly — the SIGN, remembering levels are depth below
ground so monsoon recharge makes the number smaller.
Then propose the function signature. No implementation yet.
```

**Sanity check your own output:**
```
Here's 60 days of my generated data spanning the monsoon: [paste]
Does this look like a real groundwater hydrograph? What's wrong with it?
Be specific about the shape, not just "looks fine".
```

**Day 2, performance:**
```
Inserting 131,400 rows with sqlite3 is taking minutes. Explain why committing
per row is slow — what is actually happening on disk each time?
Then show me the executemany pattern. Under 20 lines.
```

**Day 3, faults:**
```
Day 3: inject sensor faults. Explain what each fault actually looks like in a
real DWLR record — stuck sensor, spike, telemetry gap — before writing anything.
Then show me the stuck-sensor injection only, under 20 lines. I'll do the others.
Important: do NOT set quality_flag. P1's detector has to find them unaided.
```

**Day 4, verification:**
```
I built a 0.6 m/yr decline into station PB-001. P1's calculate_trend() returns <X>.
Help me work out whether that's agreement or a bug. For each possible mistake —
slope still in metres per day, sign flipped, spikes not excluded — tell me what
number I'd expect to see.
```

## Learning (chat, not IDE)
```
Explain how a time series decomposes into trend + seasonal + noise, using an
Indian groundwater hydrograph as the example. Why is the monsoon rise sharp and
the recession slow? What would look physically wrong to a hydrogeologist?
```
