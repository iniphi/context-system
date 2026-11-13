---
name: start
description: Open a work session. Use when the owner types /start or @start, says "let's start" or "where was I", or begins work for the day. Reads the index, the state page and the last log, says where things stand, and asks what today is for. The first time, interviews the owner and fills in the state page.
---

# Start a session

Short and warm. One question at a time.

## First time? (`context/state.md` still has empty lines under "Me")

1. Say in three lines what this repo does: it remembers the project between sessions, in small files the owner can read too, and saves them to GitHub.
2. Interview them, one question at a time, waiting for each answer:
   - What do you do, in a line?
   - How do you like things explained?
   - What are you making, in a line?
   - What would "done" look like?
   - What should the first session achieve?
3. Write the answers into `context/state.md` in their words, with "Where I left off" naming the first step. Show it and ask if it sounds right.
4. If they named things to do, write each as a file in `todo/` (format in `AGENTS.md`, "Headers").
5. Rebuild the index (`python tools/build_index.py`) if you can run commands.

Then go to "Today".

## Returning

1. Read `index.md`, `context/state.md` and the newest file in `log/`.
2. If you can run commands: `git pull`, so this laptop has the latest. If git reports a conflict, stop and explain it.
3. Say back, in three lines at most: what they are making, where they left off, and the next step. Mention any open to-do that is high priority or due within a week.

## Today

Ask one question: "What do you want to have by the end of this session?" If they are unsure, offer `brainstorm`. Then begin with the smallest useful step.
