# Practitioner survey: file-based context systems for AI agents

> Source: a Sonnet research agent dispatched from the GLAMhack cloud session of 2026-11-13, web only. Copied here unedited below this note. Secondary sources and UNVERIFIED marks are the agent's own; nothing in it was re-checked by hand.

Date: 2026-11-13. Method: 26 searches and fetches (bound was 30). Where a claim rests on a secondary write-up rather than the primary source, it is marked. Anything not verified is marked UNVERIFIED.

## 1. Design notes

### 1.1 AGENTS.md (the agents.md spec)
One line: an open "README for agents", plain Markdown at the repo root, read by most coding agents.
- Layout and header: no required fields or headings at all. Nested AGENTS.md files in subfolders are allowed; the nearest file to the edited file wins, and an explicit user prompt overrides everything. Suggested sections: overview, build and test commands, code style, testing, security.
- Loaded at start: the whole file (and its ancestors). There is no on-demand tier in the spec itself.
- To-dos, state, logs: not addressed. It is an instruction file, not a memory.
- Staleness and conflicts: not addressed.
- Evidence: the site claims over 60k open-source projects, and a long list of supporting tools (Codex, Jules, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Junie, Amp, Cursor, Roo, Gemini CLI, Copilot agent, Windsurf, Augment). It is stewarded by the Agentic AI Foundation under the Linux Foundation. Source: https://agents.md
- Relevant to you: Claude Code reads AGENTS.md directly from v2.1.277, but the docs recommend keeping a `CLAUDE.md` containing `@AGENTS.md` where sessions cannot read it directly, and a symlink is unsafe on Windows (git checks it out as a one-line text file). A CLAUDE.md that merely says "read AGENTS.md" in words is weaker than an `@` import, because Claude only sees it if it chooses to open the file. Source: https://code.claude.com/docs/en/memory

### 1.2 Claude Code memory: CLAUDE.md, rules, auto memory
One line: instruction files loaded at launch, plus an agent-written memory directory with an index.
- Layout: CLAUDE.md at project, user and org scope; `.claude/rules/*.md` with optional `paths:` YAML frontmatter (the only field Claude Code reads there); `@path` imports up to four hops deep.
- Loaded at start: all CLAUDE.md files in full (up to 4 MiB), unscoped rules, and the first 200 lines or 25 KB of `MEMORY.md` in the auto-memory directory. Imports do not reduce cost, because imported files load with the importer. Topic files beside `MEMORY.md` are read on demand.
- Size guidance: under 200 lines per CLAUDE.md; move anything procedural or area-specific into a skill or a path-scoped rule.
- State and logs: auto memory is `MEMORY.md` as "index, one line per memory" plus one topic file per memory. It is per machine, under `~/.claude/projects/<project>/memory/`, not in the repo.
- Source: https://code.claude.com/docs/en/memory

### 1.3 Claude Code skills (SKILL.md)
One line: on-demand procedures with a two-tier load.
- Layout: `.claude/skills/<name>/SKILL.md` with sibling reference files and scripts. Frontmatter: `name`, `description` (recommended), optional `disable-model-invocation`, `allowed-tools`, `paths` and others. Unknown keys are ignored in Claude Code; claude.ai uploads accept only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` and hard-error on anything else.
- Loaded at start: only name and description, truncated at 1,536 characters combined. The body loads on invocation and stays in the conversation. Keep SKILL.md under 500 lines; put detail in sibling files.
- `disable-model-invocation: true` removes the skill from the listing entirely (user-typed only).
- Source: https://code.claude.com/docs/en/skills

### 1.4 Cline memory bank
One line: six Markdown files that the agent is told to read at the start of every task.
- Layout: `memory-bank/` with `projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`, in a stated hierarchy (brief feeds the others; `activeContext` and `progress` change most). Instructions live in `.clinerules/` or custom instructions.
- Loaded at start: all of it, every task.
- State: `activeContext.md` (current focus, next steps) and `progress.md` (done, left, issues), updated after sessions or when asked to "update memory bank".
- Staleness: left to the agent and the user. Practitioner complaints (anecdotal): it costs tokens on every small task (one blogger prices `activeContext.md` alone at about $0.037 per read on Claude), and goes stale if not updated; one Reddit user dropped it after a few weeks. A vendor article (Fast.io, commercial interest) recommends selective-reading rules instead.
- Evidence: official Cline docs, widely copied. Sources: https://docs.cline.bot/prompting/cline-memory-bank ; https://kangax.substack.com/p/memory-bank-and-the-many-failures ; https://fast.io/resources/cline-memory-bank-guide/
- Relevant to you: this is the closest published analogue to `context/state.md` plus `log/`, and its weak point (read everything, every time) is exactly what your goal rules out.

### 1.5 Cursor rules
One line: `.cursor/rules/*.mdc` with frontmatter that decides when each rule loads.
- Header: `description`, `globs`, `alwaysApply`. Four modes follow: always (alwaysApply true; globs and description ignored), by glob, agent-chosen by description, manual by `@rule-name`. Plain `.md` files are skipped for lack of frontmatter. Docs suggest rules under 500 lines.
- Loaded at start: only always-rules; the rest by trigger. Third-party guides say vague descriptions make agent selection unreliable.
- Sources: https://cursor.com/docs/context/rules ; https://www.morphllm.com/cursor-rules-best-practices

### 1.6 Codex and Gemini CLI context files
- Codex: per directory, checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback names, at most one file per directory. Combined size is capped by `project_doc_max_bytes`, 32 KiB by default; truncation is silent. Source: https://developers.openai.com/codex/guides/agents-md . The root-down concatenation order and the global `~/.codex` override come only from third-party write-ups (UNVERIFIED against the official reference): https://codex.danielvaughan.com/2026/03/26/agents-md-advanced-patterns/
- Gemini CLI: `GEMINI.md` hierarchy (global, project and ancestors, subdirectories), concatenated and sent with every prompt; `@file.md` imports (Markdown only); `/memory show|refresh|add|list`; `context.fileName` in `.gemini/settings.json` can be an array, for example `["AGENTS.md","GEMINI.md"]`. Sources: https://geminicli.com/docs/cli/gemini-md/ ; https://agents.md
- Implication: a silent byte cap means an over-long start-up file can be truncated without warning in Codex. Keep the always-loaded part small enough to fit under 32 KiB on every tool.

### 1.7 Karpathy's "LLM wiki" pattern
One line: raw sources, an LLM-maintained wiki, and a schema file (CLAUDE.md or AGENTS.md), with `index.md` and `log.md` as the two navigation tools.
- Layout and header: `index.md` catalogues every page with a link, one-line summary and optional metadata, grouped by category; the model reads it first when answering and then opens relevant pages. `log.md` is chronological and append-only, entries prefixed consistently, for example `## [2026-04-02] ingest | Title`, so `grep "^## \[" log.md | tail -5` gives the last five.
- Scale: the gist says the index is enough at roughly 100 sources and a few hundred pages without embeddings; beyond that it suggests a search tool such as qmd (local BM25 plus vector). A secondary critique notes a drifting index misleads rather than merely under-informs (UNVERIFIED as to the original author; from a secondary summary).
- Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f ; secondary: https://zby.github.io/commonplace/sources/karpathy-llm-wiki.ingest/
- Adoption: spawned many community repos; the largest I found is claude-obsidian (below). I did not verify the gist's own star or view count.

### 1.8 Obsidian plus Claude Code vaults
One line: a vault is a folder of Markdown; Claude Code is launched inside it and a root CLAUDE.md acts as the vault manifest.
- Layout: typical PARA-style numbered folders (Claudesidian: `00_Inbox`, `01_Projects`, and so on, plus `Templates/` with project and daily-note templates); custom commands in `.claude/commands/`. Frontmatter fields suggested by guides: `status`, `project`, `type`, `tags`, enabling filtered queries (the Dataview plugin itself was not confirmed in what I read).
- Loaded at start: CLAUDE.md only; everything else found by reading folders and files.
- MCP: community servers exist (mcp-obsidian, obsidian-claude-code-mcp, second-brain-mcp), but one guide notes Claude Code does not need MCP when run inside the vault; MCP mainly serves Claude Desktop (secondary source).
- Evidence: claude-obsidian shows 16.4k stars on GitHub (fetched page; my first search snippet said 3,190 from a stale mirror, so use the fetched figure). Sources: https://github.com/AgriciDaniel/claude-obsidian ; https://cdn.jsdelivr.net/gh/heyitsnoah/claudesidian@main/README.md ; https://www.journaldunet.com/en/1557287-how-to-build-a-second-brain-for-claude-code-using-obsidian/
- Not found: any well-documented Logseq-with-agents setup or Zettelkasten-in-git template with real adoption. I did not search further (budget). Treat as a gap.

### 1.9 context-engineering-intro (coleam00)
One line: template with CLAUDE.md for global rules, `INITIAL.md` for a feature request, `examples/` for code patterns, and `/generate-prp` and `/execute-prp` commands producing a "Product Requirements Prompt".
- Evidence: about 12.5k stars per one listing; figures conflict across mirrors, so UNVERIFIED. Source: https://www.sourcepulse.org/projects/8816241
- Relevant: shows that non-trivial adoption goes to templates with a named workflow, not to bare file conventions.

### 1.10 Letta (MemGPT): core, recall, archival, and now MemFS
One line: a context window treated as RAM; Letta's own move has been from labelled blocks towards a git-backed Markdown filesystem, which is close to your design.
- Classic design: core memory is labelled text blocks with character limits, pushed into the prompt every turn; recall (conversation history) and archival (indexed knowledge) are pull surfaces the agent must search. Self-management needs a capable model, and the agent has to manage space itself (third-party review). Sources: https://www.letta.com/blog/agent-memory ; https://zby.github.io/commonplace/agent-memory-systems/reviews/letta/
- MemFS (context repositories): memory is a git repo of Markdown files with YAML frontmatter (`name`, `description` confirmed on the docs page). The file tree is always in the system prompt, so names and paths act as navigation. Files in `system/` (older layout) or at the memory root are loaded in full every turn; directories with their own `MEMORY.md` stay out of context until needed. Agents promote or demote files by moving them. Each memory edit is a commit; subagents work in separate git worktrees and merge back. The defragmentation skill targets 15 to 25 focused files. Sources: https://www.letta.com/blog/context-repositories ; https://docs.letta.com/concepts/memfs
- Not stated: how conflicts are actually resolved or any hard size limit for the pinned set (the pages do not say). A third-party review calls MemFS early (UNVERIFIED for current state).

### 1.11 Conflict-avoidance patterns for Markdown task and log files
Mostly blog posts, no benchmark.
- One file per entry (task, session, event) is the commonly recommended fix, because append-only single files conflict whenever two branches both append; kadence stores tasks as append-only event files in git (its own conflict figures disagree across listings). Another guide (session-continuity) uses TASKS.md, append-only LOG.md and git, and notes single logs grow too large to read; a suggested fix is short and newest-first.
- One writer says conflicts are rare with long gaps between sessions, and the problem starts when a shared todo file is used as a queue.
- Sources: https://chriscalo.github.io/dev-skills/skills/prompt-engineering/session-continuity ; https://agent-master-handbook.vercel.app/en/guides/conflict-prevention/index.md ; https://tasksmd.github.io/tasks.md ; https://peerlist.io/bogutskiandriy/project/kadence

### 1.12 Does a context file even help? (one study, included because it bears on size)
ETH Zurich and LogicStar, arXiv 2602.11988, ICLR 2026. LLM-generated context files lowered success slightly (about 0.5 points on SWE-bench Lite, about 2 on AGENTbench) and raised cost by over 20%; developer-written files gained about 4 points on AGENTbench, with more steps. Repository overviews did not speed file location; files helped most for non-standard practices. Python-only, specific models. Sources (secondary summaries): https://heise.de/-11245317 ; https://aiweekly.co/node/5405 ; https://iclr.cc/virtual/2026/10021142

## 2. Synthesis

### (a) Patterns that recur
1. A small always-loaded core and a larger on-demand store. Claude Code (CLAUDE.md under 200 lines, MEMORY.md index capped at 200 lines or 25 KB), Cursor (alwaysApply versus glob or description), Letta (root or `system/` pinned, the rest fetched), skills (description only at start).
2. An index that points, with one-line entries. Claude `MEMORY.md`, Karpathy `index.md`, Letta's root `MEMORY.md` and file tree.
3. Frontmatter as a router, not as metadata for its own sake. The one field that does the work in Cursor, skills and Letta is `description`; it is what the agent reads to decide whether to open the file.
4. Logs are append-only and parseable by prefix (Karpathy's `## [date] kind | title`).
5. One file per unit when several writers exist (kadence, the conflict-prevention guides, Letta worktrees).
6. Stable instructions are written by humans; agent-generated bulk context tends to hurt (ETH study, one study only).
7. A single canonical instruction file with thin pointers from tool-specific names (`@AGENTS.md`, Gemini `context.fileName`).

### (b) Choices that differ, and the trade-off
- Read everything (Cline) versus read an index (Karpathy, Letta). Reading everything is simple and robust for a weak model but costs tokens every task and rots; the index approach is cheap but depends on the index staying true.
- Who curates memory: the agent (Letta, Claude auto memory) versus the human (AGENTS.md, Cline in practice). Agent curation scales but needs a capable model and drifts; human curation is accurate but is skipped. Non-technical users are the weak link in the human option, so the close skill must do the updating.
- One log file versus one file per session. Single is easy to read and grep but conflicts and grows; per-session removes conflicts but needs an index or a naming scheme to browse.
- Strict schema (Letta name and description; skills) versus none (AGENTS.md). Strict is queryable; none is portable and forgiving.
- Retrieval: grep over index (Karpathy, up to about 100 sources and a few hundred pages) versus search tooling later. Your deterministic goal sits on the index side; the scaling ceiling is a few hundred files.

### (c) Recommendations for the draft layout
1. Keep the draft's shape; it matches what Letta converged on (Markdown, frontmatter, git) and Karpathy's schema file plus log.
2. Add `index.md` (or make `context/index.md`): one line per file in `context/`, `todo/`, `done/`, and the last N logs, each with the file's `description`. Have the `close` skill regenerate it by script, not by the model, so it cannot drift. This addresses the main staleness risk noted in the Karpathy critique.
3. Define the start-up load explicitly and cap it. Suggest: AGENTS.md under 150 lines, `context/state.md` under about 60 lines, plus the index. Total well under Codex's 32 KiB default and under Claude's 200-line guidance per file. Put the cap in AGENTS.md and have `close` check it.
4. Make `state.md` hold only what changes slowly (who, what, where I left off) and push everything else out. "Where I left off" is the single most volatile field; keep it at the top and one short paragraph.
5. Fixed frontmatter, minimal. Suggest for every file: `description` (one line, used by the index), `updated` (ISO date). Logs: `date`, `summary`. To-dos: `status` (open or done), `due` (optional), `created`. Keep names to `name`/`description` where a file is also a skill, so claude.ai uploads do not hard-error.
6. Log filenames sortable and unique: `log/2026-11-13-0930-short-slug.md`; to-dos `todo/<slug>.md` with a move to `done/` on completion. One file per entry gives conflict-free commits for several people or devices.
7. Add `context/decisions.md` or `decisions/` with one file per decision (what, why, date). Agents lose rationale across sessions; none of the reviewed designs has it as a first-class file, but Cline's `systemPatterns.md` and Karpathy's log partly cover it. This is my inference, UNVERIFIED as a proven need.
8. Put a one-line summary header in each log file and have `start` read only the newest one or two, then follow links on demand.
9. Archive rule: after N logs (say 30) or a size threshold, `close` moves old logs to `log/archive/YYYY-MM/` and keeps the index pointing at them. Handles the "single log too big" complaint and keeps directory listings short.
10. CLAUDE.md should be `@AGENTS.md` (an import), not a sentence of prose and not a symlink, per the Claude Code docs. Mention `GEMINI.md` or `context.fileName` for Gemini CLI in the README.
11. Skills: keep each SKILL.md short and put the one-question-at-a-time or interview logic in sibling files; descriptions put the trigger first (1,536 character cap). Consider `disable-model-invocation: true` on `close` so it only runs when the user types it (note: this hides it from the listing; the user needs to know the command). Check that skills work on non-Claude surfaces; on those, AGENTS.md should also say in plain words what each routine does, since skill loading is Claude-specific. Other tools' skill support is UNVERIFIED here.
12. A small script (`tools/index.py` or similar, standard library only) that rebuilds the index, lists open to-dos, and finds the latest log. Deterministic access for agents that have a shell; the same facts must also be readable by agents that only read files (claude.ai).

### (d) What argues against the draft
- Evidence that context files help is thin and mixed. The ETH study found generated files hurt and hand-written ones help modestly, mainly for non-standard practices. For a project context (personal facts, intent, state) rather than repo conventions this may not apply, but it is not tested; the design should keep the always-loaded part minimal and hand-written.
- Staleness is the real failure mode (Cline reports). A system that depends on the user or the model to update `state.md` and the index will rot. The close routine needs to be hard to skip, and scripted where possible.
- Per-session log files accumulate. With no archive rule, directory listings and the index grow without bound; Karpathy's own ceiling for index-only navigation is a few hundred pages.
- One repo per person means no shared view of state across people or projects; if several projects per person arise, you need a root index across repos. Not addressed by any reviewed design.
- Non-technical users: git commits, branches and the GitHub connection are the likeliest points of failure, and none of the practitioner designs surveyed solved onboarding for non-developers. UNVERIFIED that no such design exists; I did not search for it.
- Skills portability: SKILL.md is a Claude-specific mechanism; frontmatter beyond the allowed list hard-errors on claude.ai uploads. Keep skills thin and the rules in AGENTS.md.
- Gaps in this survey: no primary check of Logseq, Zettelkasten-in-git or Dataview adoption; no star count for the agents.md repo itself; Letta MemFS limits not documented in what I could fetch.
