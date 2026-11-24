# start (team)

A prompt any agent can follow at the start of a work session in a team repo. It adds three things to the solo loop (DESIGN.md, section 2): who is working, their own to-dos, and anything a teammate handed them. The store here is a GitHub repo laid out as in `todos.md`; another store changes how each step is done, never whether.

Short and warm. One question at a time.

## 1. Who is working

Ask: "Who's working today?" Take the first name and find `people/<name>/`. If it is missing, ask whether they are new; if yes, copy `people/_template/` to `people/<name>/` and make `work/<name>/`, and tell them.

On a machine one person always uses, the name may already be known (for example from `git config user.name`): say it and ask them to confirm, rather than ask from scratch.

## 2. Get the latest

If you can run commands: `git pull`. If git reports a conflict, stop and explain it in plain words before anything else.

## 3. Read, in this order

1. The repo's own rules (`AGENTS.md` or `CLAUDE.md`, whichever exists).
2. `people/<name>/todo.md`, the `Open` section. Lines from someone else (not `from me`) are hand-offs: read those out first, newest first, with who sent them.
3. `people/<name>/state.md`: where this person left off.
4. The shared `state.md`: where the team's work stands, and who is working on what (claims).

Read nothing else yet. What loads at the start stays small.

## 4. Say it back

In at most five lines:

- the hand-offs waiting for them (who, what), if any;
- their other open to-dos, at most three, nearest first, and a count of the rest;
- where they left off, and the very next step;
- anything in the shared state that touches their work (someone else holds a claim on it, a decision changed it).

## 5. Ask one question

"What do you want to have by the end of this session?" If a hand-off is waiting, offer it as the answer. Then begin with the smallest useful step.

If they pick up something others might also work on, add a claim line to the shared `state.md` (`- <what> · <name> since <YYYY-MM-DD HH:MM>`). A claim informs; it never blocks, and after a day it is stale.
