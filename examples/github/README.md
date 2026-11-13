# Example: solo, GitHub, a project

The first kit, built 2026-11-13 in the GLAMhack playground as `kit/`. It is now a worked example of one answer to the interview (one person, a project, stored on GitHub), not the product: see `../../DESIGN.md`, section 0. Its tests pass where it stands (`python -m pytest examples/github/tests`). Paths below that say `kit/` mean this folder.

## The choices this example made (Bradley, 2026-11-13; the first two are now one option among several, not rules)

- **One repo, the person's project.** The context lives inside the repo they work in. Most people have one project and will port it in; attaching a second repo is a step too many.
- **GitHub is the backend.** Commits give the session history for free, it stores any file type, and almost every LLM surface has a git connection. claude.ai conversations can write to repos (checked by Bradley); ChatGPT and Gemini not yet checked.
- **Plain markdown with a small YAML header**, so the system is deterministic: fixed paths, fixed header fields, readable by any agent and filterable by a script without search.
- **The simple shape first.** The estate's full skills are the quarry for later, ported by what each rule protects against, not by length.

## What the kit is

```
AGENTS.md            the rules; every agent reads it first
CLAUDE.md            one line, @AGENTS.md
index.md             one line per file, rebuilt by tools/build_index.py
context/state.md     who I am, what I'm making, where I left off
log/                 one file per session
todo/  done/         one file per to-do; closing one moves it
decisions/           one file per decision, with its reason
.claude/skills/      start, task, close, brainstorm (name + description only)
tools/build_index.py rebuilds index.md; --check validates headers and size caps
tools/install.py     adds the kit to an existing repo without overwriting anything
tests/               the kit's own tests
```

Three things came from the survey (`research/`): the script-built index (a hand-kept index drifts, and a drifting index misleads), hard caps on what loads at the start (Codex silently truncates context files past 32 KiB), and skills whose header holds only `name` and `description` (claude.ai rejects other keys on upload). `decisions/` is the survey's suggestion too, marked there as unproven.

The ETH Zurich result (arXiv 2602.11988, v3 read 2026-11-13: context files do not generally raise coding agents' success, LLM-written or developer-written, and cost over 20% more; their instructions are followed, their overviews do not help) is answered in `AGENTS.md` by one rule: record what happened and what was decided, never a summary of what the files already show. The survey's earlier "hand-written ones helped" was a secondary summary and is wrong for v3; see `research/2026-11-13-stacks-picks-read.md`, which also raises Skill Leakage: the close procedure sits in both `AGENTS.md` and the `close` skill.

## Two ways in

1. **A new project:** "Use this template" on GitHub.
2. **An existing project:** `python tools/install.py <their-repo>` from a copy of the template. A dry run by default (`--apply` writes); it never overwrites a file. Their own `AGENTS.md` is kept and gets a pointer block, with the kit's rules in `CONTEXT.md`; `CLAUDE.md` imports the rules by name (`@CONTEXT.md` or `@AGENTS.md`), never by a prose pointer; `.gitignore` gains only the missing lines. It refuses before writing anything if a kit folder (`log/`, `todo/` and so on) already holds non-context files, or a skill of the same name exists. Built 2026-11-13; tried on a copy of the GLAMhack repo (refused: four clashes, its own `start`/`close`/`brainstorm` and `log/README.md`) and on a small repo with house rules (installed, check OK).

Not built: the same route for someone with no shell (a chat writing through a connector). The plan `install.py` prints is the recipe such an agent would follow by hand.

## Open

- Three research questions: does the ETH result hold beyond coding agents and Python repos; what does the evidence say about start-up load size against task success; is structured or one-file-per-entry memory measured anywhere, or only advised. A literature search on 2026-11-13 gave five papers (`research/2026-11-13-stacks-picks-read.md`). Question 3 came back empty and is still open.
- A log archive rule (index-only navigation holds to a few hundred files).
- Optional extras for the tech-savvy: a GitHub Action that runs `build_index.py --check` on every push (costs Actions minutes on a private repo), a Notion mirror, Obsidian as a viewer (the kit is already a valid vault).
- Whether ChatGPT and Gemini connectors can write.
