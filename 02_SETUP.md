# 02 — Setup (Day 0 — everyone, ~1 hour)

No React means no Node, no npm, no `node_modules`. The install list is tiny.

---

## Install

| Tool | Get it | Check with | Want |
|---|---|---|---|
| **Python** | python.org — **3.14.0 or newer** | `python --version` | 3.11+ |
| **Git** | git-scm.com | `git --version` | 2.40+ |
| **GitHub account** | github.com | log in | — |
| **A browser** | Chrome or Firefox | — | — |
| **Antigravity** | already installed | opens | — |
| **DB Browser for SQLite** *(optional, useful)* | sqlitebrowser.org | opens | — |

> **Windows:** when installing Python, tick **"Add Python to PATH"**. Skipping it causes half of all day-1 problems.
> On some systems the command is `python3` and `pip3` rather than `python` and `pip`. Both are fine — just be consistent.

Post the output of `python --version` and `git --version` in the team channel. All six, before Day 1.

---

## Git identity (once per machine)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main
```

**GitHub won't accept your password for pushes.** You need a **Personal Access Token**:
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new → tick `repo` → copy it.
When git asks for a password, paste the token. Save it somewhere — GitHub only shows it once.

---

## Repo setup — P1 does this once

```bash
mkdir groundwater-app && cd groundwater-app
git init
```

Create `.gitignore` **before the first commit**:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
*.db
*.sqlite3
.env
.DS_Store
.idea/
.vscode/
```

Why each line matters:
- `.venv/` is machine-specific and large — it won't even work on someone else's operating system.
- `*.db` is your local database. Six people each committing their own copy of a **binary** file creates conflicts Git cannot merge. The database is *generated*, so it never belongs in Git.
- `.env` holds secrets. **Once a secret is pushed it is public forever**, even if you delete it in the next commit.

```bash
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin https://github.com/<you>/groundwater-app.git
git push -u origin main
```

Then everyone else: `git clone <url>`.

---

## Python environment (P1, P2, P3, P6)

```bash
cd groundwater-app
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

You know it worked when your prompt starts with `(.venv)`. **Activate it in every new terminal** — forgetting is the most common "why isn't this installed" moment.

`requirements.txt`:
```
fastapi
uvicorn[standard]
numpy
pandas
```

Four packages, and that's the whole backend. `numpy` is for P1's maths and P3's generator; `pandas` is for P6's CSV checking. `sqlite3` is built into Python — nothing to install.

Also create an **empty file** `backend/__init__.py`. It's what makes `backend` importable as a package, so `from backend.analytics import calculate_trend` works and `uvicorn backend.main:app` finds your app. Without it you'll get `ModuleNotFoundError` and lose twenty minutes to it.

---

## Running things

**You need two terminals open at once.** This surprises people the first time.

**Terminal 1 — backend** (from the repo root, venv active):
```bash
uvicorn backend.main:app --reload
```
Then open `http://127.0.0.1:8000/docs` — FastAPI generates an interactive page listing every endpoint, where you can click "Try it out" and see real responses.

> **P4 and P5: `/docs` is your manual. Keep that tab open all day.** It shows you the exact shape of every response, so you never have to guess a field name.

**Terminal 2 — frontend** (from the `frontend/` folder):
```bash
cd frontend
python -m http.server 5500
```
Then open `http://127.0.0.1:5500`.

> ⚠️ **Do not double-click the HTML file to open it.** Opening as `file://` makes `fetch()` fail for security reasons, and the error message doesn't say so clearly. **Always serve it.** This will confuse someone around Day 3 — it's this.

**Ports:** backend on 8000, frontend on 5500. Because they're different ports, the browser treats them as different origins — which is why P2 must enable **CORS** on the backend from Day 2. Without it, the browser silently refuses to load your data.

---

## Who needs to learn what (be realistic — this is 10 days)

**Everyone — 2 hours, Day 0:**
- `05_GIT_QUICKSTART.md` and the exercise at the end
- `01_BRIEF_AND_SCIENCE.md` §6, and answer the six questions

**P1, P2, P3** (already comfortable coding): skim FastAPI's tutorial intro and Python's `sqlite3` docs. Pick up the rest as you go.

**P4, P5, P6** (beginners) — 6–8 hours across Days 0–1. **This is the plan, not a delay.**
1. **JavaScript basics** (4 h) — variables, functions, arrays, `for` / `forEach`, objects, then `fetch()` with `async`/`await`. Skip classes, modules, and everything else.
2. **DOM basics** (2 h) — `document.getElementById`, `.textContent`, `.innerHTML`, `addEventListener`, and **opening the browser console with F12**.
3. **HTML/CSS** (2 h) — enough to lay out a page with flexbox.

That's genuinely all the frontend knowledge this project needs.

**Best possible use of your learning time:** get one HTML page that calls any public API with `fetch()` and puts the result on the screen. Once you've done that once, every other frontend task in this project is the same move repeated.

**Free resources — pick one per topic, don't collect them:** MDN's *JavaScript first steps* · javascript.info chapters 1–5 · MDN's *Introduction to the DOM* · the official FastAPI tutorial · SQLBolt for SQL.
