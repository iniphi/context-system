# context-system: design before build

Started 2026-11-13 in the GLAMhack playground, moved here the same evening. The aim is to work the system out for the agents before building it. The first kit (now `examples/github/`) answered one case: one person, project work, GitHub, a fixed format. This file widens that to any purpose, any store, solo or team, and keeps the start/close loop as the core.

## 0. Ruled (Bradley, 2026-11-13)

1. **No fixed format, no fixed store.** The `start` and `close` routines carry the essentials of the loop (section 2) and apply them to whatever store the person chooses. The earlier "GitHub is the backend" and "plain markdown with a fixed header" are withdrawn as rules.
2. **GitHub is the first recommendation**, for its usefulness: history in every commit, fixed paths, no conflicts between writers. The README makes the case; people are free to ignore it.
3. **Version one supports every store by being prompts, not code.** Like an 85Labs kit: staged prompts, the few code snippets strictly needed (gists), and customisation prompts. The GitHub kit is a worked example (`examples/github/`), not the product.
4. **Two folders: `solo/` and `team/`.**
5. **Public as soon as possible** (amended the same evening; it was "private until the design is settled"). Created as `iniphi/context-system` (private) on 2026-11-13, carrying the staging folder's history.
6. **A chat-only version** (same evening): most chats can at least read a public repo, so a pasted line installs a version that needs no connector. Its store is the person: a save block they keep and paste back (`solo/chat.md`). This is why it goes public early.

## 1. What the system is

A loop, set up for one person or one team by a short first-time interview.

- **The loop**: every session opens by reading where things stand and closes by writing it back. That is the part learned the hard way, and everything else serves it.
- **The routines are prompts.** `start` and `close` say *what* must happen at each step. How a step is done (a file, a Notion row, a Doc) is set by the store the person chose.
- **The interview** asks, one at a time: what is this for (section 3), where will it live (section 4), just you or a team (section 5). The answers are kept in the store, so a later session on any surface knows what kind of system it is in without asking again.

## 2. The loop: what `start` and `close` must carry, in any store

These are the essentials. A store adapter may change *how*, never *whether*.

**`start`**
1. Read the system's own rules.
2. Read where things stand (the state).
3. Read the record of the last session.
4. Say back, in three lines at most, where things stand and the very next step.
5. Ask one question: what is today for.
6. First time only: the interview, then write the state in the person's own words.

**`close`**
1. Rewrite where things stand (never append), ending with the very next step.
2. Write a new record of this session; never edit an old one.
3. File new to-dos and decisions in the one place each lives; move finished to-dos to done, never delete them.
4. Show the person what changed and ask if anything is wrong.
5. Check nothing private or secret is in what is saved.
6. Save, then read the save back. A success message is not proof.
7. End with one line: what got done, and what is next.

### The lessons behind them

Each cost real sessions before it became a rule.

| Lesson | What went wrong before it | Where it lives in the loop |
|---|---|---|
| A session that does not close leaves the next one cold | Work was done and the next session could not find it or why | `close` runs every time, named or not |
| "Where I left off" is rewritten, never appended | Appended state grew until nobody read it, and old lines contradicted new | `close` 1 |
| One entry per record | Two sessions appending to one list collided, and one list grew past reading | `close` 2 and 3 |
| An index is built by a script, not by the model | A hand-kept index drifted and then misled | store adapters, where the store allows a script |
| Write what happened and why, never a summary of what the work already shows | Summaries went stale; a study found agent-written overviews do not help and cost more (arXiv 2602.11988) | the rules `start` 1 reads |
| A decision is kept with its reason | Agents reopened settled questions because the why was lost | `close` 3 |
| A to-do lives in one place only | To-dos written inside pages were orphaned when nobody reopened the page | `close` 3 |
| A write is not done until it is read back | A tool reported success and changed nothing (seen on Notion's API more than once) | `close` 6 |
| A fact is checked or labelled unchecked | Confident wrong claims were caught only when the owner pushed back | the rules |
| One copy is canon; any other is a mirror | Two "sources of truth" drifted, and nobody could say which was right | the interview records which is canon |
| Ask one question at a time | A wall of questions at the end of a reply got skimmed or half-answered | everywhere |
| Keep what loads at the start small | Large start-up files cost tokens on every task, and one tool cuts them off silently (Codex, 32 KiB) | `start` 1 to 3 only |

Worth adding later from the estate, not in v1: claims before contested work (team), and the morning review of unattended work.

## 3. Interview, question one: what is this for?

The part of the person's life the system should improve. It decides what the state holds, what the store keeps beyond the loop, and what `close` asks before it ends.

| Purpose | The trouble it answers | What the loop adds | Kept beyond the loop; extra routines |
|---|---|---|---|
| **Focus** | Starting over every session; drifting off the one thing that matters | `start` names the single next step; `close` will not end without one | the state opens with the next step; `park` notes a distraction without following it |
| **Scattered brain** | Many threads at once; forgetting what is in flight | Capture fast, sort later; `close` sweeps the inbox | an inbox, threads with a status; `capture`, `sweep` (weekly) |
| **Writing** | Ideas lost between drafts; the argument goes missing | Each piece carries its argument forward, not just its text | pieces, each with outline, drafts, notes; `outline` (sentence outline), `draft`, `revise` |
| **Ideation** | Good ideas evaporate, or never meet each other | Every idea kept, with a status and its links | ideas (seed, growing, parked, used); `brainstorm`, `connect` |
| **Learning or study** | Reading that does not stick | Notes from each source, questions kept open | sources, questions; `recall` (asks back) |
| **A project** | The project's state lives in one head | The first kit, as it is | as `examples/github/` |
| **Something else** | Said in the person's own words | The agent proposes a shape and asks before building it | recorded with the answers |

- More than one answer is allowed, but the agent asks which comes first and builds only for that. A second purpose is added later by asking again.
- The person's own words are kept next to the label, so the agent works from what they meant, not from the menu.
- Unsure defaults to **Focus**, the smallest shape.

## 4. Interview, question two: where will it live?

Where the record is **stored** (the canon) is kept apart from what the person **looks at** it with (a viewer). Obsidian is a viewer over a folder; the folder is the store.

The agent offers GitHub first and makes the case in a sentence or two, then takes whatever the person picks. Every store is judged on the same lines: can an agent read and write it from the surfaces people use; does it keep history; what happens when two writers meet; can a team share it; how hard it is to set up for someone who is not technical.

| Store | Store or viewer | Agent writes from | History | Two writers | Team | Setup for a non-developer |
|---|---|---|---|---|---|---|
| GitHub (recommended) | store | Claude Code; claude.ai chat (checked by Bradley); others not checked | full, every commit | clean with one entry per file | good | hardest (git) |
| Local folder (plus OneDrive, iCloud or Dropbox) | store | Claude Code, Claude Desktop; no phone chat | only the sync service's | "conflicted copy" files | weak | easiest |
| Obsidian | viewer over a folder or repo | as the store underneath | as the store | as the store | weak | easy |
| Notion | store | claude.ai and Claude Code by connector; others not checked | in the app, not to an agent | real-time, few conflicts | very good | easy |
| Google Drive | store | claude.ai by connector; Gemini (not checked) | per file, in the app | real-time in Docs | very good | easy |
| claude.ai Project | store, Claude only | that Project's chats | little | n/a | team plans (not checked) | none at all |
| A database, e.g. Supabase | store | any agent with a key or a connector | as built | safe | very good | needs a developer |

"Not checked" means exactly that: each is a test to run before the kit claims it works.

### The case for GitHub (what the README says)

Every save is a commit, so the whole history is there for free; fixed paths mean an agent never has to search; one entry per file means two people or two devices never collide; private repos are free; Claude Code works in it natively and a claude.ai chat can commit to it; a team reviews through pull requests. The cost is git itself, the biggest hurdle for someone who is not a developer, and the kit's GitHub example is written to carry them past it.

### Each store, for its adapter prompt

- **GitHub.** For: as above. Against: git for non-developers; no comfortable phone route except through a chat; a committed key or a public/private slip is a real risk.
- **Local folder.** For: nothing to sign up for, plain files that last, offline, Claude Code and Desktop read it directly. Against: no phone or browser chat can reach it; sync services leave "conflicted copy" files the agent must look for; weak for teams.
- **Obsidian.** For: a pleasant reader with links, backlinks and a graph; plugins can read headers (Dataview); free for personal use. Against: it is a viewer, so an agent reaches the notes only through the store underneath (a folder, git, or the paid Obsidian Sync); chat surfaces need an MCP server. Offer it on top of GitHub or a folder.
- **Notion.** For: the friendliest surface for non-developers; to-dos and decisions become databases with views and dates; a good phone app; built for teams; claude.ai's connector reads and writes. Against (measured on the estate): writes can fail silently, so every write is read back; large writes hit parse errors and firewall blocks; pages are found by id, not path, so the adapter keeps a list of them; history is not available to an agent; Markdown round trips are lossy; to-dos typed inline get orphaned; the integration is shared page by page.
- **Google Drive.** For: nearly universal; sharing and comments are familiar; real-time editing; a claude.ai connector that creates and updates files; Gemini built in. Against: a Doc is not plain text; file names are not unique, so ids are tracked; one Doc per to-do is heavy (a Sheet suits lists); history is per file and not to an agent.
- **claude.ai Project.** For: no setup; instructions and knowledge load into every chat. Against: Claude only; as far as known a chat cannot write back into the Project's knowledge, so `close` has nowhere to save (UNVERIFIED: check first). Best as a halfway house: the Project holds the rules, the store is elsewhere through a connector.
- **A database.** For: structured, queryable, safe with many writers. Against: needs a developer; nothing to read without a front end; a misplaced key is a breach.

**One store is canon; a second is a mirror and is marked as one.** "GitHub and Notion" is allowed only as canon plus a one-way mirror written by `close`.

## 5. Interview, question three: just you, or a team?

The two folders.

### `solo/`

One writer, perhaps several devices or surfaces. Conflicts come from devices, not people. The state is about the person.

### `team/`

What changes when more than one person writes:

- **Whose state**: a shared state for the work, and one per person for their own "where I left off". Each close rewrites only its own and the parts of the shared one it changed.
- **Names on records**: who owns a to-do, who wrote a log, who made a decision.
- **Handoffs are not to-dos**: a message to a teammate is addressed to them, and their `start` reads anything addressed to them first.
- **Claims**: work in progress says who has it and since when, so two people do not do the same job. A claim informs, never blocks, and goes stale after a day.
- **Private and shared**: a teammate's own notes stay out of the shared store, and `close` never copies them across.
- **Store fit**: a team pushes towards GitHub, Notion or Drive.
- **Scope**: small teams, two to five people.

## 6. Layout

Ruled: `solo/`, `team/`, and the GitHub kit as an example. Proposed (not ruled) for the rest:

```
README.md              what it is, the case for GitHub, how to begin
DESIGN.md              this file
solo/                  the routines for one person: start, close, the interview
team/                  the same for a team, plus handoffs and claims
stores/                one customisation prompt per store: how each loop step is done there,
                       its for and against, the few snippets it needs     (proposed)
purposes/              one prompt per purpose: what it adds to the state and the routines  (proposed)
examples/github/       the first kit, a worked example of solo + GitHub + project
research/              the survey and the read papers behind the lessons
```

`stores/` and `purposes/` are shared by `solo/` and `team/`, so each is written once.

## 7. Still open

1. Whether `stores/` and `purposes/` sit beside `solo/` and `team/` (as proposed) or inside each.
2. The purpose list: whether Learning and Project stay, and whether job search or life admin belongs.
3. How someone with no shell installs it: the route is pasting a prompt into a chat that has a connector to their store. Its wording is the first thing to write.
4. Which stores get tested first for agent write access (ChatGPT and Gemini are unchecked everywhere).
5. When it goes public.
