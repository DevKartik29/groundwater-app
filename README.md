# Groundwater App — 10-Day Build Kit
### SIH25068 · Real-Time Groundwater Resource Evaluation Using DWLR Data · Team of 6

**Goal:** a small app that works, that all six of you understand. Not a hackathon-winning submission — a project you learn the workflow from.

---

## What you're building

**Two screens.** A map of 30 groundwater monitoring stations coloured green/yellow/red. Click one → a page showing its water-level chart, how fast the water table is falling, how much recharge came in last water year, and how many readings look like sensor faults.

**Stack:** Python + FastAPI + SQLite + plain HTML/CSS/JavaScript. Chart.js and Leaflet from a CDN.
**No React. No npm. No build step.** Two installs total: Python and Git.

---

## The files

| File | What | Who |
|---|---|---|
| **`00_PROJECT_OVERVIEW.md`** | **What this project is**, in plain language, no prior context needed. Hand this to a mentor, a judge, or anyone who asks. | Everyone + outsiders |
| **`01_BRIEF_AND_SCIENCE.md`** | What we build, the stack, the minimum groundwater science. **Ends with 6 questions everyone must answer** (answers included). | Everyone |
| **`08_HOW_IT_ALL_WORKS.md`** | **The complete walkthrough** — what the user sees, and exactly what happens between a click and a chart. **Read this second.** | Everyone |
| **`02_SETUP.md`** | Install checklist, git config, how to run both servers | Everyone |
| **`03_ROLES_AND_PLAN.md`** | The 6 roles + the day-by-day plan | Everyone |
| **`04_API_CONTRACT.md`** | 5 endpoints, 2 database tables | P1–P5 |
| **`05_GIT_QUICKSTART.md`** | Git from zero, team workflow, conflicts | Everyone |
| **`06_PROMPTS.md`** | Tool split + the 6 prompts you need | Everyone |
| **`07_TROUBLESHOOTING.md`** | Every error this stack actually produces, with fixes | Everyone |
| **`AGENTS.md`** | Rules for Antigravity → repo root | The agent |
| **`PROGRESS.md`** | The tracker → repo root | Everyone |
| **`agents/AGENT_01–06_*.md`** | One short file per person | Its owner |

Keep these **in the repo**, not in a chat thread. The agent reads files; it can't read your chat history.

**Reading order for a new team member:** `00` (what this project is) → `01` (what and why, in detail) → `08` (how it all fits together) → `02` (get set up) → `05` (git) → your own `agents/AGENT_0X_*.md` → `03` (the plan). Then `04` and `07` as you need them.

---

## Do these five things today

1. **P1 creates the repo** with `.gitignore`, `AGENTS.md`, `PROGRESS.md`, the folder skeleton from `01_BRIEF_AND_SCIENCE.md` §4, and an empty `backend/__init__.py`.
2. **Assign the six roles** and send each person their `agents/AGENT_0X_*.md`.
3. **Everyone installs Python + Git** and posts their version output.
4. **Everyone reads `01_BRIEF_AND_SCIENCE.md` §6 and answers the 6 questions.**
5. **Everyone does the Git exercise** — one merged PR each, before any app code exists.

---

## The five things most likely to decide whether this works

**1. Day 0 discipline.** A day where nobody writes app code feels wasted on a 10-day project. It's the opposite — it's what stops someone still fighting `pip` on Day 6.

**2. `mock.json` on Day 1.** P2 hand-writes three fake stations in fifteen minutes. Without it, P4 and P5 sit idle until Day 3 — a third of your team, for a third of your time.

**3. Day 3.** Map → click station → real chart. If that whole path doesn't work by end of Day 3, stop adding features and fix it. Everything after Day 3 is decoration on that one path.

**4. The reversed y-axis.** Water level is *depth below ground* — bigger is worse. Get the chart backwards and it looks completely normal while saying the exact opposite of the truth. Nothing errors. Which is why, in projects like this, it usually survives all the way to demo day.

**5. Day 4's cross-check.** P3 built a known decline into the data, so P3 is the only person who can tell whether P1's trend function is right. One hour, and it catches the unit bug that would otherwise reach the judges.

---

## Two sentences that make the project honest

*"The live 6-hourly DWLR feed sits behind WIMS, which is restricted to authorised agencies. Our app reads from a database — connect the real feed and nothing else changes."*

*"Specific yield is a standard value for the rock type, not a site measurement, so treat the recharge figures as approximate."*

Both are true, both are the correct engineering answer, and both are much stronger than hoping nobody asks.

---

## Numbers used consistently throughout this kit

So you can spot a typo if you ever see a different one:

| | |
|---|---|
| Stations | **30** |
| Record length | **3 years**, 6-hourly |
| Readings per station | **4,380** |
| Total readings | **131,400** |
| Demo station | **PB-001**, Ludhiana, Punjab, `alluvium_sandy`, Sy **0.14** |
| Its trend | **0.62 m/yr** falling → `critical` |
| Its recharge | Δh **1.2 m** → **168 mm** (≈23% of ~730 mm rainfall ✓) |
| Its anomalies | **44** of 4,380 (**1.0%**) |
