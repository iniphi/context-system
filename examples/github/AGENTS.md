# AGENTS.md - read this first

This repo is a project with a memory. You are an AI agent working with its owner. Everything you need to pick up where the last session stopped is in a few small files, at fixed places, with fixed headers. Read them; do not guess.

Never create another `AGENTS.md` or `CLAUDE.md` anywhere in the repo: a nearer one hides this one. (In a repo that had its own `AGENTS.md` first, these rules live in `CONTEXT.md`, and that `AGENTS.md` points here.)

## At the start of every session

Read exactly these, in order, and nothing else until you need it:

1. This file.
2. `index.md`: one line for every context file, open to-do, decision and recent session.
3. `context/state.md`: who the owner is, what they are making, where they left off.
4. The newest file in `log/`.

Then say back, in three lines at most, where things stand and what the next step is, and ask what today is for. Open any other file only when the index says it matters for today's work.

## Where things live

| Path | Holds | One file per |
|---|---|---|
| `context/` | Standing facts: `state.md`, and any other page the owner wants loaded on demand | topic |
| `log/` | What happened in a session | session |
| `todo/` | Things still to do | to-do |
| `done/` | Finished to-dos, moved here from `todo/` | to-do |
| `decisions/` | What was decided and why | decision |
| `index.md` | A list of all of the above, built by a script | (one file) |

One file per entry is the rule that keeps this working. Two sessions, or two people, never edit the same lines, so git never reports a conflict. Never collect entries into one shared list.

## Headers

Every file in those folders starts with a YAML header between `---` lines. These fields are required; add others if useful, never remove these.

```yaml
# context/<topic>.md
description: one line, what this page is for
updated: 2026-11-13

# log/<YYYY-MM-DD-HHMM>-<slug>.md
date: 2026-11-13
summary: one line, what this session did

# todo/<YYYY-MM-DD>-<slug>.md   (the date is the day it was logged)
description: one line, what needs doing
status: open
created: 2026-11-13
priority: normal          # high, normal or low; optional, normal if absent
due: 2026-11-20           # optional

# done/<same name as in todo/>
...as the to-do, with status: done and closed: 2026-11-14

# decisions/<YYYY-MM-DD>-<slug>.md
description: one line, the decision
date: 2026-11-13
```

The body under the header is free: a few lines of plain prose. A decision's body says why, and what else was considered.

## What to write, and what not to

Write what the files cannot tell a later reader on their own: what happened, what was decided and why, what was tried and failed, what the owner prefers. Never write a summary of what the project's files already show (its structure, its code, its contents): a later agent can read those itself, and a summary goes stale and misleads.

Keep `context/state.md` under 60 lines. Rewrite it at each close; do not append. History goes in `log/`, reasons in `decisions/`.

## Closing a to-do

Move the file from `todo/` to `done/` (same name), set `status: done`, add `closed:` with today's date. Never delete a to-do: `done/` is the record of what got finished and when.

## At the end of every session

Read `.claude/skills/close/SKILL.md` and follow it, every time, whether or not the owner names it and whether or not your tool has a skill system. The steps live there only, so there is one copy to keep true.

## Saving

**With a shell** (Claude Code, OpenCode, Codex, Gemini CLI):

```
git status
git add <name each file>         # never "git add ." or "-A"
git commit -m "<what this session did, in plain words>"
git push
```

**Through a connector** (a chat with GitHub access): commit the changed files to the repo in one commit with the same kind of message.

Never force-push, never rewrite history, never delete a branch, without the owner asking in so many words. If git says something you do not understand, stop and explain it; do not try to fix it.

## Rules that always hold

- No key, password or token in any file. Keys go in `.env`, which git ignores.
- No personal details about other people (addresses, emails, phone numbers) in a committed file.
- A number or fact you state comes from something you ran or read this session. Otherwise say it is not checked.
- Ask one question at a time.
- Before deleting or overwriting anything, say what, and wait for a yes.

## Routines

The owner can name these. Each is a file in `.claude/skills/<name>/SKILL.md`; if your tool has no skill system, read that file and follow it.

- `start`: open a session (the steps at the top of this file, plus a first-time interview).
- `task`: open a session on a job the owner can already name.
- `close`: end a session; the only copy of the closing steps.
- `brainstorm`: think something through, one question at a time, ending in two or three small next steps.
