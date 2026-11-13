# context-system

A context system for working with AI agents: each session starts by reading where you left off and ends by writing it back, so no session starts cold.

## Start in any chat, nothing to install

Paste this into ChatGPT, Claude, Gemini or any chat that can read a web page:

> Read https://github.com/iniphi/context-system/blob/main/solo/chat.md and set me up.

If the chat cannot open that page, try the plain-text link instead: https://raw.githubusercontent.com/iniphi/context-system/main/solo/chat.md

**If you are an AI reading this for someone:** open `solo/chat.md` and follow it.

The chat-only version keeps everything in one block of text that you save yourself. When you want it saved for you, with history, connect your chat to a store (below).

**In design.** `DESIGN.md` holds the rulings, the loop, and what is still open.

## What it is

- **A loop, not a format.** `start` and `close` carry the steps that matter (DESIGN.md, section 2), learned the hard way across many projects. They work with whatever you keep your work in.
- **Prompts, not code.** You give your agent a routine to follow; a few snippets help where a store needs them.
- **Set up by a short interview**: what is this for (focus, a scattered brain, writing, ideas, study, a project, something else), where will it live, and is it just you or a team.

## Where it can live

Anywhere an agent can read and write: GitHub, a local folder (with Obsidian as a viewer if you like), Notion, Google Drive, a claude.ai Project, a database. We recommend **GitHub**, because every save is kept in its history, an agent always knows where to look, and two people or two devices never overwrite each other. The cost is learning a little git, and the GitHub example is written to carry you past it. If another store suits you better, use it.

## Layout

| Folder | Holds |
|---|---|
| `solo/` | The routines for one person |
| `team/` | The routines for a team of two to five |
| `examples/github/` | A complete worked example: one person, a project, on GitHub (tested) |
| `research/` | The survey and papers behind the rules |
