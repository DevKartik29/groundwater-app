# 05 — Git Quickstart

Read this before writing any code. All six. ~45 minutes including the exercise.

Git is where beginner teams lose the most time — not because it's hard, but because everyone learns just enough to commit, and then one conflict on day 6 eats an afternoon you don't have.

---

## The idea in one picture

```
  your files  ──git add──►  staging  ──git commit──►  your history  ──git push──►  GitHub
                                                            ▲
                                                            └──git pull──  (others' work)
```

- **Commit** = a snapshot with a message. Once committed, your work is safe.
- **Branch** = a movable label pointing at a commit. Creating one is instant and free.
- **`main`** = the branch that must always work. Nobody commits to it directly.

**The reassuring truth: if you committed it, it's almost certainly recoverable.** So commit often. The only genuinely dangerous states are uncommitted work and force-pushes.

---

## The 10 commands you need

```bash
git status                  # WHAT IS GOING ON. Run it constantly.
git clone <url>             # get the repo, once
git pull                    # bring down others' work
git switch -c feat/thing    # create and move to a new branch
git switch main             # move to an existing branch
git add <file>              # stage a file  (git add . stages everything — check status first)
git commit -m "msg"         # snapshot
git push -u origin <branch> # first push of a branch
git push                    # every push after that
git log --oneline -10       # recent history
```

That's the job. Look the rest up when you hit it.

> Use `git switch` for branches, not `git checkout`. `checkout` does six unrelated things and is most of the reason Git feels confusing.

---

## Your daily loop

```bash
# start of the day — always from an up-to-date main
git switch main
git pull

# branch for what you're about to do
git switch -c feat/station-chart

# ...work... commit whenever something works, not once at the end
git add frontend/station.js
git commit -m "feat: station chart with reversed y-axis"

# before pushing, get the latest main
git pull --rebase origin main

# push, then open a Pull Request on GitHub and tag P1
git push -u origin feat/station-chart

# after it's merged
git switch main && git pull
```

**Branch names:** `feat/...` new thing · `fix/...` bug · `docs/...` writing · `data/...` datasets.
Lowercase, hyphens. `feat/rahul-work` tells nobody anything.

**Commit messages:** `type: what changed, imperative`

```
✅ feat: add /api/stations endpoint
✅ fix: reverse chart y-axis
✅ data: add 30 CGWB stations
❌ update      ❌ final      ❌ asdf      ❌ fixed bug
```

If your message needs the word "and", it should have been two commits.

---

## Merge conflicts — don't panic

Happens when two people changed **the same lines of the same file**. Git can't guess who's right, so it asks.

```
<<<<<<< HEAD
const API = "http://127.0.0.1:8000";
=======
const API = "https://our-app.onrender.com";
>>>>>>> feat/deploy
```

Above `=======` is **yours**. Below is **theirs**.

**Fix:** edit the file so it's correct, **delete all three marker lines**, then `git add <file>` and `git rebase --continue`. Then actually run the code — a conflict that resolves cleanly isn't necessarily resolved *correctly*.

**Panic button:** `git rebase --abort` puts you back exactly where you were. Nothing lost.

**Having fewer conflicts:**
1. **Edit only your own files** (`03_ROLES_AND_PLAN.md`). This alone prevents ~90% of them.
2. `git pull --rebase origin main` at the start of every session.
3. Merge every evening. A branch that lives 4 hours doesn't conflict; one that lives 4 days does.
4. We deliberately gave P4 and P5 **separate JS files** (`station.js` and `map.js`) so they can never collide. The only shared frontend file is `shared.js`, which P1 owns and which should barely change after Day 1.

---

## Pull requests

Every change reaches `main` through a PR. Yes, including P1's — someone else reviews the lead.

**PR description — three lines, always:**
```
What: adds the station detail chart
Why this way: Chart.js because it's one CDN tag; y-axis reversed per the science doc
Can I explain every line? yes / no — if no, say which part
```

**That last line is the whole point of this project.** If it isn't honestly "yes", say so and ask for a walkthrough. Nobody will judge you for that. Ticking it falsely and then freezing when someone asks how your code works — that gets noticed.

**P1: review within a few hours.** On a 10-day timeline a stale PR is a blocked teammate, and a blocked teammate is 17% of your capacity.

---

## When Antigravity runs Git for you

1. **Read every command before approving it.** Don't know what it does? Ask, then approve.
2. **Never approve** `git push --force`, `git reset --hard`, or `git checkout .` unless P1 says so. These delete work permanently.
3. **The agent must never commit to `main`.**
4. When it says "committed and pushed", run `git log --oneline -5` yourself. Trust, verify.

---

## Emergency recipes

| Problem | Fix |
|---|---|
| Committed to `main` by mistake (not pushed) | `git branch feat/oops` → `git reset --hard origin/main` → `git switch feat/oops` |
| Bad commit message (not pushed) | `git commit --amend -m "better message"` |
| Undo last commit, keep the changes | `git reset --soft HEAD~1` |
| Need to switch branches mid-work | `git stash` … later … `git stash pop` |
| Committed `.venv` or the `.db` file | `git rm -r --cached .venv` (or `git rm --cached groundwater.db`), fix `.gitignore`, commit |
| Pushed a secret | Tell P1 immediately and rotate the key. It's public now. |
| Completely lost | Clone fresh into a new folder. Your old folder still has everything. |

---

## Exercise — everyone does this before Day 1

1. Clone the repo
2. `git switch -c docs/<yourname>`
3. Create `docs/team/<yourname>.md` with your role and your answers to two of the six science questions
4. `git add`, `git commit` with a proper message, `git push -u origin docs/<yourname>`
5. Open a PR with the three-line description
6. Get it reviewed and merged
7. `git switch main && git pull`
8. Post your `git log --oneline -5` output in the channel

**Nobody starts Day 1 until all six have done this.** Thirty minutes now, or an afternoon lost on Day 6.
