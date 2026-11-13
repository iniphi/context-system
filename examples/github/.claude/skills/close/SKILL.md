---
name: close
description: End a work session. Use when the owner types /close or @close, says "let's stop", "save my work" or "I'm done for now", or a session is ending. Rewrites where things stand, writes the session log, files to-dos and decisions, rebuilds the index, checks nothing private is included, and saves to GitHub.
---

# Close a session

Say what each step does in one line as you do it. The owner should see their work saved, and know where it went.

1. **State.** Rewrite "Where I left off" in `context/state.md`: two or three lines, ending with the very next step. Set `updated:` to today. Keep the page under 60 lines.
2. **Log.** A new file `log/<YYYY-MM-DD-HHMM>-<slug>.md` with `date` and `summary` in its header, then: did, worked, did not work, next. Never edit an old log.
3. **To-dos and decisions.** New ones as new files. Finished to-dos move to `done/` with `status: done` and `closed:` (see `AGENTS.md`, "Closing a to-do"). A decision's file says why.
4. **Show them** the changed state page and the log, and ask if anything is wrong.
5. **Index.** `python tools/build_index.py`, then `python tools/build_index.py --check`. Fix every PROBLEM line it prints before saving. With no shell, edit `index.md` by hand in the same format and say so in the log.
6. **Safety.** No key, password or token; no personal details about other people; nothing the owner said is private.
7. **Save** in one commit, as `AGENTS.md`, "Saving" says: name each file, plain-words message, push. If the push is refused, stop and explain; never force it.

End with one line: what they did today, and what is next.
