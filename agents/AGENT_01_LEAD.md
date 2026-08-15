# AGENT_01 — P1: Lead + Analytics

> Read `AGENTS.md` first. **Skill level: comfortable with code.** Explain concepts once, briefly, then move.

## Mission
Own the four numbers the app displays, and make sure six people's work fits together.

If someone asks "how did you get that recharge figure?", you answer.

## You own
```
backend/analytics.py       the maths + the SPECIFIC_YIELD dictionary
frontend/shared.js         API base URL, fetchJSON(), formatDepth()
04_API_CONTRACT.md         final say
AGENTS.md · PROGRESS.md
all PR reviews · the evening merge
```
You don't write API routes (P2), the generator (P3), or any page-specific JS.

**Key design rule:** `analytics.py` takes plain lists in and returns plain dicts out. **No database code inside it.** That way you can test every function with 20 hand-made numbers and no server running — which on a 10-day timeline is the difference between finding a bug in 2 minutes and in 2 hours.

---

## Your four functions + one dictionary

```python
SPECIFIC_YIELD = {
    "alluvium_sandy":     0.14,
    "alluvium_silty":     0.08,
    "sandstone":          0.05,
    "weathered_granite":  0.025,
    "basalt":             0.015,
}
# THE single source of truth. P2 imports this on Day 2 to fill the DB column.
# Commit it on Day 1 even though the functions are still empty — P2 is blocked without it.

def calculate_trend(dates, levels) -> dict
    # fit a line to daily averages; slope in METRES PER YEAR
    # positive slope = depth increasing = water table FALLING = bad

def calculate_recharge(dates, levels, specific_yield) -> dict
    # water year = 1 June to 31 May
    # delta_h = max(levels in that year) - min(levels in that year)
    # recharge_mm = delta_h * specific_yield * 1000

def detect_anomalies(levels) -> dict
    # stuck: 12+ identical consecutive values
    # spike: far from the local median

def get_status(slope_m_per_year) -> str
    # < 0.1 -> "safe" | 0.1-0.3 -> "watch" | > 0.3 -> "critical"
```

Each function is ~15 lines. **Write the test before the function** — hand-calculate the answer on paper first, then assert it. Write the function first and you'll unconsciously write a test that agrees with whatever it happens to do.

---

## ⚠️ Two traps in your own code

**1. The units trap.** If you feed `numpy.polyfit` an x-axis of *days since the first reading*, the slope comes out in **metres per day**. Multiply by **365.25**. Forget it and you get a number ~365× too small, which reads as "no trend" and is very easy to miss because nothing errors. P3 will catch it on Day 4 by comparing against the decline they built in — but you should catch it first.

**2. Excluding bad readings.** Flagged readings (`SPIKE`, `STUCK`) must be **excluded from the trend and recharge maths** but **kept in the database and shown on the chart**. A single 4 m spike inside a 24 m series will wreck both a max−min recharge calculation and a line fit. Filter them out inside your functions; don't ask P2 to delete them.

**Suggested simple spike rule** (keep it robust, not clever): compare each reading to the median of the 11 readings around it; flag if the difference exceeds 2 m or 5× the median absolute deviation, whichever is larger. Explain it in one sentence in `docs/methodology.md`.

---

## Day plan

| Day | Do |
|---|---|
| 1 | `04_API_CONTRACT.md` written and sent. Function signatures + docstrings. **`SPECIFIC_YIELD` committed — P2 needs it tomorrow.** `frontend/shared.js`. |
| 2 | `calculate_trend()` + test on a series with a known slope |
| 3 | `calculate_recharge()` + test (Δh 1.2 m × 0.14 → 168 mm) |
| 4 | `detect_anomalies()` + `get_status()`, checked against P3's known-broken rows |
| 5 | Review everything. Grep for the depth-vs-elevation bug. Hand-verify every displayed number. Confirm P4's y-axis is reversed. |
| 6 | Empty and error states across the whole app |
| 8 | `docs/methodology.md` — where each number comes from, formula, assumptions, uncertainty |
| Daily | PR reviews within hours · run the evening merge · keep `PROGRESS.md` true |

**One naming decision to make on Day 1:** `/api/stations` returns `trend_m_per_year` and `/analytics` returns `slope_m_per_year`. **Pick one name for both.** Two names for one number will cost somebody twenty confused minutes. Recommendation: `trend_m_per_year` everywhere.

---

## Traps

| Trap | Instead |
|---|---|
| Doing the beginners' work when they're slow | Pair 20 minutes. Never take the keyboard. If you write P4's chart, P4 learned nothing and you own it for 10 days. |
| Reviewing PRs once a day | Hours, not days. A stale PR blocks 17% of your team. |
| Making the analytics clever | Four simple functions that are provably right beat sophisticated ones nobody can check. |
| Committing `SPECIFIC_YIELD` on Day 3 | Day 1. P2's Day-2 loader needs it. |
| Letting the contract drift verbally | Change it in the file *and* announce it in the channel. |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_01_LEAD.md, and PROGRESS.md.
Two sentences: what day, what's next. One question if needed. No code yet.
```

**Before writing a function:**
```
Day <N>, backend/analytics.py, calculate_recharge().
Before code:
1. State the formula and every input.
2. List edge cases: fewer than one full water year, all readings flagged,
   delta_h of zero, missing specific_yield, an unknown formation name.
3. Propose the signature and the return dict.
Wait for my approval.
```

**Tests first:**
```
I'm hand-calculating two recharge cases. Help me build input series where the
expected output is unambiguous, then write the assertions.
Do NOT write calculate_recharge() yet.
```

**Checking the units trap:**
```
My calculate_trend returns 0.0017 for a station I know declines ~0.6 m/year.
Don't fix it. Walk me through where a unit conversion could go wrong between
days, years, and metres, and tell me what number I'd expect for each mistake.
```

**Reviewing a beginner's PR:**
```
Here's a diff from a beginner teammate. Review against AGENTS.md §4 (domain
rules) and §6 (done means). Give me concerns as QUESTIONS I can ask them —
I want them to find it themselves.
[paste diff]
```

**Deciding something:**
```
Decision needed: <X>. Give me 2-3 options, one line of trade-off each, your
recommendation with a reason, and what it costs us if we're wrong.
Under 150 words. Then I decide.
```

## Learning (chat, not IDE)
```
Explain the Water Table Fluctuation method as if I'm implementing it tomorrow:
the formula, why delta_h is ambiguous, and three ways teams get it wrong.
Then quiz me with 3 questions.
```
