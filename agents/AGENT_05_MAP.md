# AGENT_05 — P5: Map Page

> Read `AGENTS.md` first.
> **⚠️ COMPLETE BEGINNER** at both web development and maps. Agent: explain every concept the first time, including the map ones. Max 30 lines per reply. Quiz after every step.

## Mission
The map is the first thing anyone sees. **Thirty dots, coloured green/yellow/red, and you understand India's groundwater situation in three seconds.** That's more than any chart does.

## You own
```
frontend/index.html
frontend/map.js
```

You have your **own** JS file — you and P4 will never touch the same file, so you can't get merge conflicts with each other. The one shared file is `frontend/shared.js` (P1's): it holds the `API` base URL and helpers. Use them; don't redefine them. Ask P4 before editing `style.css`.

---

## What you're building

One page:
- A **Leaflet** map centred on India
- 30 station markers, **coloured by status** — 🟢 safe, 🟡 watch, 🔴 critical, ⚪ grey when unknown
- Click a marker → popup with name + latest level → link to `station.html?id=PB-001`
- A legend
- (Day 5) a station list beside the map; clicking either one highlights the other

Leaflet loads from a CDN — **two tags, not one.** You need the `<link>` for its **CSS** *and* the `<script>` for its JavaScript. Load only the JS and the map renders with controls in strange places and misaligned tiles, with no error to tell you why.

---

## 🚨 The thing that will bite you

**Leaflet uses `[latitude, longitude]`.** GeoJSON and several other map tools use `[longitude, latitude]` — the reverse. Mix them up and every Indian station lands in the ocean off Somalia.

**India's real bounds: latitude 6 to 37, longitude 68 to 98.**

Write this check on Day 2. Five lines, and it turns a confusing hour into an instant answer:

```js
if (s.lat < 6 || s.lat > 37 || s.lon < 68 || s.lon > 98) {
  console.warn("Suspicious coordinates:", s.station_id, s.lat, s.lon);
}
```

---

## Day plan

| Day | Do |
|---|---|
| 0–1 | JavaScript + DOM basics. Then a Leaflet map of India with 3 hardcoded markers. |
| 2 | Markers from `mock.json`. Click → popup with the station name. Add the coordinate check. |
| 3 | Switch to the real API (one line in `shared.js`). All 30 stations. Click → opens `station.html?id=...` |
| 4 | Colour the dots by `status`. Add a legend. |
| 5 | Station list next to the map, two-way highlight |
| 6 | Sensible zoom, readable popups, works in a small window |

> **Day 3 note:** until P2 runs `refresh.py` on Day 4, `status` comes back as `null`. **Default to grey** rather than waiting — write the colour function so an unknown status is grey, and Day 4 fills the colours in automatically with no code change.

---

## One call, not thirty

`GET /api/stations` returns everything you need for every marker in **one request** — position, status colour, and popup text.

```js
const stations = await fetchJSON(`${API}/api/stations`);
stations.forEach(s => { /* one marker per station */ });
```

Don't loop and call the API once per station. Thirty requests where one would do is the most common beginner mistake with APIs, and it's visibly slower.

---

## Traps

| Trap | Instead |
|---|---|
| `[lon, lat]` instead of `[lat, lng]` in Leaflet | Add the bounds check on Day 2 |
| Loading Leaflet's JS but not its CSS | Both tags. The map looks subtly broken with no error. |
| Map container has no height | Leaflet needs an explicit height in CSS (`#map { height: 600px; }`) or it renders as a blank strip. Start with pixels, not percentages. |
| One API call per station | One call, loop over the result |
| Opening `index.html` by double-clicking | Serve it: `python -m http.server 5500`. `file://` breaks `fetch()`. |
| Adding markers before the map object exists | Create the map first, then add markers |
| Waiting for the backend | `mock.json` exists from Day 1 |

---

## Your prompts

**Session start:**
```
Read AGENTS.md, agents/AGENT_05_MAP.md, and PROGRESS.md.
I'm a complete beginner at web development and maps. Two sentences:
what day, what's next. One question if needed. No code yet.
```

**Day 1, first map:**
```
Day 1: a Leaflet map of India in index.html.
Before code, explain in plain language: what a tile server is (where do the map
images actually come from?), what zoom level 5 looks like versus 10, and why the
map container needs a height in CSS.
Then show me only: the two CDN tags (CSS and JS), the div, and the map
initialisation. Under 25 lines. Centre on India.
```

**Day 2, markers:**
```
Day 2: draw a marker for each station in mock.json.
Explain first: what does .forEach() do, and why is one API call better than one
call per station?
Then show me the loop skeleton with comments — I'll write the marker code myself.
Remember: Leaflet takes [lat, lng] in that order.
```

**Day 4, colours:**
```
Day 4: colour each marker by its status field (safe/watch/critical), with grey
as the default when status is null.
Explain the options for coloured markers in Leaflet (circleMarker vs custom icons)
and which is simpler for a beginner. Recommend one, then show me the
colour-picking function only.
```

**When it breaks:**
```
Not working: [what you see] [any red text in the browser console] [what I did]
Do NOT give me fixed code. Tell me: what does this error mean in plain English,
the 3 most likely causes ranked, and what do I check first? Then wait.
```

> Open the console first (**F12 → Console**) and check `07_TROUBLESHOOTING.md` — the map section covers the grey box, the misaligned tiles, and the stations-in-the-ocean problem.

**Finishing:**
```
That looks done. Quiz me with 2 questions about it, then update PROGRESS.md.
```

## Learning (chat, not IDE)
```
I'm a beginner. Explain how a web map works: what tiles are, where the images
come from, what zoom levels mean, and what latitude and longitude actually
measure. Under 400 words. Then quiz me.
```
```
Explain fetch() and async/await with a tiny example that gets a list from an API
and loops over it. Then ask me to explain it back and correct me if I'm vague.
```
