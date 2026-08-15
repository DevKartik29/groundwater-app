# AGENT_04 — P4: Station Page + Charts

> Read `AGENTS.md` first.
> **⚠️ COMPLETE BEGINNER.** Agent: explain every concept the first time. Max 30 lines per reply. Never assume they know what `async`, `fetch`, or `getElementById` mean. Quiz after every step. If they seem lost, slow down — don't push forward.

## Mission
The station page is what the demo actually shows. **You own the screen everyone will be looking at.**

## You own
```
frontend/station.html
frontend/station.js
frontend/style.css        (P5 asks you before editing)
```

You have your **own** JS file — you and P5 will never touch the same file, so you can't get merge conflicts with each other. The one shared file is `frontend/shared.js` (P1's): it holds the `API` base URL and helpers like `formatDepth()`. Use them; don't redefine them.

---

## What you're building

One page. Given a station id in the URL (`station.html?id=PB-001`):
- station name, state, district
- **the hydrograph** — water level over the last year
- latest reading in m bgl
- trend: "falling 0.62 m per year"
- recharge: "168 mm in water year 2025–26"
- anomaly count: "44 of 4,380 readings (1.0%) look like sensor faults"

Six things. That's the page.

**Reading the id from the URL** — one new thing to learn:
```js
const id = new URLSearchParams(window.location.search).get("id");
```
If `id` is missing or the API 404s, show a friendly message and a link back to the map. Don't let the page throw a raw error.

---

## 🚨 The one thing you must not get wrong

Water level is **depth below ground**. A bigger number means deeper water, which is worse.

**Your chart's y-axis must be REVERSED** — shallow at the top, deep at the bottom.

```js
options: {
  scales: {
    y: { reverse: true, title: { display: true, text: 'Depth (m bgl)' } }
  }
}
```

Set this on Day 2. Have P1 confirm it. Then never touch it again.

**Why this bug is dangerous:** nothing errors. The chart renders perfectly. It just quietly says the opposite of the truth — a station whose water table is collapsing looks like it's recovering. That's why it survives all the way to demo day in projects like this.

---

## Day plan

| Day | Do |
|---|---|
| 0–1 | JavaScript + DOM basics. Then a page that `fetch`es `mock.json` and prints station names. |
| 2 | `station.html` + a Chart.js line chart with hardcoded data. **Reversed y-axis.** |
| 3 | Switch to the real API (one line in `shared.js`). Read the id with `URLSearchParams`. Real data on the chart. |
| 4 | Add trend, recharge, latest reading, anomaly count |
| 5 | Flagged readings in red · loading / error / empty states |
| 6 | CSS pass · `formatDepth()` used on every number on the page |

---

## The three states — build them Day 5, don't skip

Every real screen has three states beyond "it worked":
- **Loading** — "Loading station…" while the fetch is in flight
- **Error** — "Couldn't reach the server" when it fails
- **Empty** — when the API returns `status: "not_enough_data"` or `points: []`

Most student projects show a blank white screen when anything goes wrong.
**Test yours by stopping the backend and reloading.** Thirty seconds, and it's the difference between a demo that survives an unexpected click and one that doesn't.

**When the API says `not_enough_data`, show its `reason` text.** Don't show `0` — a zero looks like a real measurement and someone will believe it. "We can't compute this yet, and here's why" is more trustworthy than a fake number, and it's a much better answer when a judge asks.

---

## Traps

| Trap | Instead |
|---|---|
| Starting with CSS | Get data on screen first, ugly. Pretty on Day 6. |
| Forgetting the reversed axis | Day 2, verified by P1 |
| Opening `station.html` by double-clicking it | Serve it: `python -m http.server 5500`. `file://` breaks `fetch()`. |
| Waiting for the backend | `mock.json` exists Day 1. You are never blocked. |
| Copying a whole file from the agent | Ask for the shape, type the logic yourself |
| Different number formatting on each line | `formatDepth()` from `shared.js`, everywhere |
| "Canvas is already in use" when data reloads | Keep a reference to the chart; `.destroy()` or `.update()` instead of creating a second one |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_04_STATION_PAGE.md, and PROGRESS.md.
I'm a complete beginner. Two sentences: what day, what's next.
One question if needed. No code yet.
```

**Starting anything (use this shape every time):**
```
Today: <thing>.
Before code:
1. What is this doing, in one sentence?
2. What data does it need and where does it come from?
3. Which new JavaScript concept does this introduce? Explain it in 4 sentences
   with a tiny example that isn't from our project.
Then show me the skeleton with comments where the logic goes — I'll write the
logic. Under 30 lines.
```

**The chart (Day 2) — use this exact prompt:**
```
Day 2: a Chart.js line chart in station.html.
CRITICAL: water level is DEPTH BELOW GROUND. Bigger = deeper = worse.
The y-axis MUST be reversed so shallow is at the top.
Explain why hydrologists draw it that way before writing anything.
Then show me: the CDN script tag, the canvas element, and the chart config with
the reversed axis. I'll wire up the data myself.
```

**Reading the URL (Day 3):**
```
Day 3: my page is opened as station.html?id=PB-001 and needs that id.
Explain what URLSearchParams is and what window.location.search contains,
in 4 sentences with a tiny example. Then show me just those two lines, plus
what to do if id is missing.
```

**When you don't understand it:**
```
Stop. Explain this line by line as if I've never seen JavaScript.
Then ask me 3 questions to check I followed it.
[paste code]
```

**When it breaks:**
```
Not working: [what you see] [any red text in the browser console] [what I did]
Do NOT give me fixed code. Tell me:
1. What does this error mean in plain English?
2. The 3 most likely causes, most likely first?
3. What do I check first?
Then wait.
```

> Open the browser console (**F12 → Console**) *before* asking, and check `07_TROUBLESHOOTING.md`. Nine times out of ten the answer is already sitting there in red.

**Finishing:**
```
That looks done. Quiz me with 2 questions about it, then update PROGRESS.md.
```

## Learning (chat with Gemini/ChatGPT — NOT the IDE)
```
I'm a beginner. Explain fetch() and async/await with a tiny example that gets a
list from an API and puts it on a web page. Then ask me to explain it back in my
own words and correct me if I'm vague.
```
```
I need to show groundwater depth on a chart where a bigger number is worse.
Explain why the y-axis is reversed, and what a viewer would misread if it weren't.
Then give me 2 other charting conventions that exist to prevent misreading.
```

> **Rule:** chat explains, the IDE builds. Never let the chat AI write code for the repo — it can't see your files and will invent a different structure.
