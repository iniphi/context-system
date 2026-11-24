# close (team)

A prompt any agent can follow at the end of a work session in a team repo. It is the solo close (DESIGN.md, section 2) with three team rules: rewrite only your own state, write anything that did not close back to its owner's to-dos, and never copy a teammate's private notes into the shared store. Layout as in `todos.md`.

Say what each step does in one line as you do it.

1. **Your state.** Rewrite `people/<name>/state.md` (never append): two or three lines on where you left off, ending with the very next step.
2. **Shared state.** Change only the parts of the shared `state.md` this session changed. Remove your own claims on work you finished or stopped; leave other people's lines alone.
3. **To-dos.** For each thing that came up and did not close in this session (and only those: `todos.md`, "Keep the bar high"):
   - yours, for a later session: a line in your own `Open`, `from me`;
   - someone else's: a line in **their** `people/<them>/todo.md`, `from <name>`. This is the hand-off. Do not leave it in a shared folder or a chat for them to find;
   - finished: move the line to `Done` with today's date. Only ever move your own lines.
4. **Session record.** A new file `log/<YYYY-MM-DD-HHMM>-<name>.md`: did, worked, did not work, handed to whom, next. Never edit an old one.
5. **Show them** what changed (their state, any hand-offs written, the log) and ask if anything is wrong.
6. **Safety.** No key, password or token. No personal details about anyone: first names only, nothing a teammate did not agree to have written down. A teammate's private notes never leave their own folder.
7. **Save** in one commit naming each file, with a plain-words message, then push. If the push is refused because someone else pushed first, `git pull` and push again; if git reports a conflict, stop and explain it; never force a push.
8. **Read it back.** Open the pushed files (or `git log -1 --stat`) and check they say what you wrote. A success message is not proof.

End with one line: what got done, what was handed to whom, and what is next.
