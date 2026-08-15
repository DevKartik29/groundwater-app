# 06 — Prompts

---

## The tool split — get this right or you'll waste a day

| Tool | Job | Sees your repo? | Writes project code? |
|---|---|---|---|
| **Antigravity + Gemini** | **Builder** — writes files, runs commands | ✅ | ✅ under `AGENTS.md` rules |
| **Gemini / ChatGPT chat** | **Tutor** — explains, quizzes, rubber-ducks | ❌ | ❌ **never** |
| **Claude (this project)** | **Architect** — design calls, stuck points, docs | ❌ | design + small snippets only |

**Why chat tools must not write your project code:** they can't see your files. They'll invent different filenames, a different folder layout, a different API shape. You paste it in, it doesn't fit, and you burn an hour reconciling two AIs' opinions. On a 10-day project that hour matters.

**Rule: chat explains, IDE builds, Claude decides.**

---

## The six prompts you actually need

### 1. Start of every session
```
Read AGENTS.md, agents/AGENT_0X_<ROLE>.md, and PROGRESS.md.
Tell me in two sentences what day we're on and what's next.
Ask one clarifying question if needed. Do not write code yet.
```
Twenty seconds. Stops the agent building yesterday's task or tomorrow's.

### 2. Before building anything
```
Today's task: <thing>.
Before any code:
1. What are we building, in one sentence?
2. What goes in and what comes out?
3. What breaks it — empty data, missing station, bad input?
4. Which new concept does this introduce? Explain it in 4 sentences with a
   tiny example that isn't from our project.
Then show me the structure only, with comments where the logic goes.
I'll write the logic. Under 30 lines.
```

### 3. When you don't understand what it wrote
```
Stop. Explain this line by line as if I've never seen this language.
Then ask me 3 questions to check I actually followed it.
[paste the code]
```

### 4. When something breaks — **the most valuable prompt here**
```
Not working: [what you see] [exact error text] [what you ran]
Do NOT give me fixed code. Instead:
1. What does this error mean in plain English?
2. The 3 most likely causes, most likely first?
3. What do I check first?
Then wait for me.
```
Every time you let the agent silently fix something, you skip a rep. Debugging is the skill that separates people who can build software from people who can only assemble it.

### 5. Finishing a task
```
That looks done. Before we move on:
1. Quiz me with 2 questions — one about an edge case, one about why we chose
   this approach.
2. Update PROGRESS.md in the AGENTS.md §7 format.
```

### 6. When it runs ahead
```
That's beyond today's task. Stick to <task>. Put the rest in the Parking Lot
in PROGRESS.md and continue with what I asked.
```
You will need this. Agents love to helpfully build the next three features.

---

## What not to say

| ❌ | Why it hurts | ✅ instead |
|---|---|---|
| "Build the whole app" | 800 lines you can't debug, and you own them | "Build `/api/stations` only. Structure first." |
| "Fix it" | You learn nothing; the bug returns in a new shape | Prompt 4 |
| "Make it better" | Undefined target → random refactoring in files you didn't ask about | "Make `/timeseries` faster. Measure first, then propose one change." |
| "Add login too" | Out of scope, and you have 10 days | Parking Lot |
| "Use React instead" | Stack is locked; five people build against it | Don't |
| Error with no context | It guesses | What you ran + expected + full error |
| Accepting code you don't get | You'll freeze when someone asks how it works | Prompt 3 |

---

## When the agent misbehaves

```
Stop. You wrote code before explaining — that's AGENTS.md §3.2.
Explain what you wrote and why, then quiz me.
```
```
That's over 30 lines. Break it into steps. Show me step 1 only.
```
```
You used a library that isn't in our stack. Redo it with only what's in
requirements.txt, or with plain JavaScript.
```
```
You said the water table is "rising" because the number went up. The number
is DEPTH BELOW GROUND. Re-read AGENTS.md §4.1 and correct yourself.
```
```
You edited a file I don't own. Revert it and tell me whose it is.
```
```
You put a specific yield number somewhere other than analytics.SPECIFIC_YIELD.
That dictionary is the single source of truth. Move it back.
```

---

## Learning prompts — chat tools, not the IDE

**Concept from zero:**
```
Explain <concept> to someone who's never seen it, in under 300 words, using
one groundwater example. Then ask me to explain it back and correct me if
I'm vague.
```

**Depth check — use this when you *think* you understand:**
```
I think I understand <concept>. Here's my explanation: <yours>.
Grade it. What did I get wrong, what did I miss, what am I overconfident about?
Be direct.
```

**Rubber duck:**
```
I'm stuck on <problem>. Don't solve it. Ask me questions until I find it.
```

**Before the demo:**
```
Act as a groundwater scientist reviewing our project. Ask me the 5 hardest
questions about our data and our methods. Then critique my answers.
```

---

## The classic bugs — keep these handy

**Nothing renders, but the API works when I open it directly:**
```
The page shows nothing, but /api/stations returns data when I open it in the
browser. Give me an ordered checklist to find where it breaks: opening the file
as file:// instead of http://, CORS, wrong API URL, a field name mismatch,
a JS error in the console. One check at a time, and tell me exactly what to look at.
```

Nine times out of ten it's one of three things: **you opened the HTML file directly instead of serving it**, **CORS isn't enabled on the backend**, or **the JSON field name doesn't match what your JS expects**. **Open the browser console (F12) first** — the answer is usually already there in red.

The full list of the errors you'll actually hit, with fixes, is in **`07_TROUBLESHOOTING.md`**. Check that before asking the agent — it'll be faster.

---

## The one rule

> **Never merge code you cannot explain.**

Not "code you didn't write" — you'll pair with the agent constantly, that's fine. **Code you can't explain.** If you can't say what it does, why it's done that way, and what would break it, you don't have a feature — you have something that will fail the first time anyone asks a question about it.

When that happens (it will), the fix is boring and takes twenty minutes: ask the agent to explain it line by line, ask it to quiz you, then delete it and rewrite it yourself from the explanation.

