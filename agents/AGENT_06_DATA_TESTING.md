# AGENT_06 — P6: Station Data + Testing + Demo

> Read `AGENTS.md` first.
> **⚠️ COMPLETE BEGINNER.** Agent: explain every concept the first time. Max 30 lines per reply. This person writes real Python — don't treat this as a non-technical role.

## Mission
**The demo works and the story is clear.** And on Day 1, the entire team is blocked on you.

Read that again, because this role can look like the leftover job and it isn't: a project that runs perfectly and is presented badly loses to a worse project presented well. You own presentation *and* the one file five people need before they can start.

## You own
```
data/stations.csv       ← Day 1, blocks P2 and P3
docs/test-checklist.md
README.md
the slide deck + demo video
```

---

## DAY 1 — the station list. Do this first, finish it today.

**30 real CGWB monitoring stations.** Real names, real districts, real coordinates.

```csv
station_id,name,state,district,lat,lon,formation
PB-001,Ludhiana Piezometer 2,Punjab,Ludhiana,30.9010,75.8573,alluvium_sandy
MH-004,Ahmednagar Observation Well,Maharashtra,Ahmednagar,19.0952,74.7496,basalt
```

> **Note there is no `specific_yield` column.** That number lives only in `analytics.SPECIFIC_YIELD`, and P2 fills the database column from there. If the value existed in the CSV *and* in the code they'd eventually disagree, and nobody would notice which one the app was actually using. Your job is the `formation` name; the code owns the number.

**Pick contrasting places** — this matters more than you'd think:

| State | `formation` | Why include it |
|---|---|---|
| Punjab / Haryana | `alluvium_sandy` | Badly over-pumped — the dramatic declining story |
| Rajasthan | `weathered_granite` | Hard rock, deep water tables |
| Maharashtra | `basalt` | Deccan trap, very low specific yield |
| Tamil Nadu | `weathered_granite` | Different monsoon timing (north-east, Oct–Dec) |
| West Bengal / Bihar | `alluvium_sandy` | Shallow, high recharge |

Thirty identical stations make a boring demo. Five different hydrogeological settings make the map *mean* something.

**Check every row before you commit:**
- No duplicate `station_id`
- **Latitude 6–37, longitude 68–98.** One typo and a station appears in the ocean.
- `formation` spelled **exactly** as in `01_BRIEF_AND_SCIENCE.md` §6b — `alluvium_sandy`, not `Alluvium Sandy` or `alluvium-sandy`. P1's lookup matches that exact string; a typo silently produces a wrong recharge number that nobody catches.
- No empty cells
- No trailing spaces (they're invisible and they break exact-string matching — `.str.strip()` everything)

Sources: CGWB's public station lists and Ground Water Year Books, India-WRIS, data.gov.in ground-water section.

---

## Day plan

| Day | Do |
|---|---|
| 1 | **`stations.csv`, 30 rows, validated.** Nothing else matters today. |
| 2 | Check P3's readings: nulls? negative depths? `station_id`s not in `stations`? |
| 3 | Test all 5 endpoints at `http://127.0.0.1:8000/docs`. File issues with repro steps. |
| 4 | Check every number on screen against the API. Hand-calculate one recharge. **Run the rainfall sanity check on all 30 (below).** |
| 5 | Write `docs/test-checklist.md` |
| 6 | Run the checklist. Log every bug. |
| 7 | Deploy the frontend to Netlify with P2 |
| 8 | `README.md` — then follow it on a clean machine, it'll be wrong, fix it. Build the deck. |
| 9 | **Demo the whole app solo.** Record the 3-minute backup video. |

---

## Day 4: the rainfall sanity check (your highest-value hour)

Groundwater recharge is normally **5–25% of annual rainfall**. For each of the 30 stations:

1. Look up the district's rough annual rainfall (one web search each, or use a state average)
2. Divide our computed `recharge_mm` by it
3. Flag anything outside 5–25%

A station showing 500 mm of recharge in a district that gets 600 mm of rain is a bug — probably an unexcluded spike, or a wrong formation string. **You are the only person positioned to catch this**, because it needs outside knowledge rather than code.

Put the table in the deck. "We validated our recharge estimates against regional rainfall and all 30 stations fall in the expected 5–25% band" is a sentence that changes how a jury listens to the rest of your talk.

---

## Day 9: you present

If the person who didn't write the backend can demo the whole thing without help, that itself proves the product works. Everyone else knows only their own piece — you're the only one who has to know the whole path.

**Demo script skeleton (5 minutes):**
1. **The problem, 30 seconds** — 4 readings a year vs 4 a day. One sentence, one number.
2. **The map, 60 seconds** — zoom to Punjab. Red. Zoom to Bengal. Green. Let the map do the talking.
3. **A station, 120 seconds** — click Ludhiana. The falling hydrograph. The trend number. The recharge number, and *say* that specific yield is an approximation.
4. **The sensor faults, 60 seconds** — the red points on the chart. "We detect when the instrument itself is wrong." This is your differentiator; don't rush it.
5. **Honesty + scale, 30 seconds** — where the data comes from, and that the same pipeline runs on the real WIMS feed unchanged.

**Prepare for the four questions you will be asked:** *Is this real data? How did you calculate recharge? How accurate is it? What happens at 5,260 stations instead of 30?*

**Record a backup video.** Venue wifi fails. Assume it will. Also remember Render's free tier sleeps — **open the live site 5 minutes before you present** or your first click is a 60-second blank screen.

---

## Bug reports that actually help

```
What I did:       Opened the map, clicked Ludhiana Piezometer 2
What I expected:  Station page with a chart
What happened:    Blank page; console says "Cannot read properties of undefined"
Where:            Chrome, deployed URL
```

"The map is broken" costs the other person a round-trip asking what you meant. On a 10-day project that round-trip is expensive.

---

## Traps

| Trap | Instead |
|---|---|
| Treating this as the non-coding role | You write Python validation scripts. Learn it. |
| Starting the CSV on Day 2 | Day 1. Five people are waiting. |
| Adding a `specific_yield` column "to be helpful" | Don't. One source of truth, and it's the code. |
| A README you never followed | Follow it on a clean machine. It will be wrong. |
| Building the deck on Day 9 | Outline it Day 5, so the team knows what story they're building toward |
| Assuming the venue wifi works | Local backup + recorded video, both ready |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_06_DATA_TESTING.md, and PROGRESS.md.
I'm a beginner. Two sentences: what day, what's next. One question. No code yet.
```

**Day 1, validating the CSV:**
```
I have a CSV of 30 groundwater station rows. I want a small Python script that
checks it before I commit.
Before code: explain what pandas is and what a DataFrame is, in 5 sentences.
Then list the checks you'd run — I'll compare against my own list.
Then show me ONE check implemented (duplicate station_ids), under 15 lines,
every line commented. I'll write the rest using it as a pattern.
```

**Day 2, checking the readings:**
```
P3 generated 131,400 readings. Help me write checks for: null values, negative
depths, readings referencing a station_id that isn't in stations, and timestamps
outside the expected 3-year range.
One check per response. After each, tell me how to run it and what the output
means. Then stop.
```

**Day 3, testing endpoints:**
```
I'm testing our 5 endpoints at /docs. Give me a checklist of what to try for each —
valid input, invalid station id, missing parameter, empty result.
What should each one return per 04_API_CONTRACT.md? I'll go through them and
report what I find.
```

**Day 4, the sanity check:**
```
Explain why groundwater recharge is typically 5-25% of annual rainfall — what
happens to the other 75-95%? Then help me build a small table comparing our 30
stations' computed recharge_mm against their districts' annual rainfall, and tell
me what an out-of-range value most likely means.
```

**Day 8, README:**
```
I'm about to follow our README on a clean machine to check it works.
List the things that commonly go missing from setup instructions — Python version,
virtual env activation, backend/__init__.py, the order of the seed steps, which
folder to run from, the two ports.
I'll check each against what we wrote.
```

**Day 9, the demo:**
```
I'm demoing a groundwater monitoring app in 5 minutes to people who work with
this data professionally. Help me structure it: what to show first, what to
leave out, how to answer "is this real data?", and how to mention our limitations
without undermining the project.
```

## Learning (chat, not IDE)
```
I'm responsible for data quality on a government-data project. Teach me the
standard checks for a tabular dataset — completeness, uniqueness, validity,
consistency — with one concrete example of each using groundwater monitoring
station data. Then quiz me.
```
