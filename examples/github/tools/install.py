"""Add the context system to a repo that already exists, without overwriting anything.

    python tools/install.py <path-to-your-repo>            show the plan, change nothing
    python tools/install.py <path-to-your-repo> --apply    do it

Run it from a copy of the context-system repo. It never overwrites a file. Where the
target already has its own rules, it adds to them between context-system markers:

- No AGENTS.md: the kit's AGENTS.md is copied in.
- An AGENTS.md of its own: the kit's rules go to CONTEXT.md, and AGENTS.md gets a short
  block telling every agent to read CONTEXT.md first.
- CLAUDE.md: created as "@AGENTS.md" if missing; otherwise a block importing the rules is
  added, unless it already imports AGENTS.md.
- .gitignore: the kit's lines that are missing are added in one block.

It stops before writing anything if a file or folder would clash: a folder the kit uses
(log/, todo/ and so on) holding files that are not context files, a skill of the same name,
or an index.md, CONTEXT.md or build_index.py that is not the kit's. Exit codes: 0 done or
planned, 1 a clash (nothing written), 2 the target is not a folder.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = ("context", "log", "todo", "done", "decisions")
NOT_SHIPPED = {"AGENTS.md", "CLAUDE.md", ".gitignore", "tools/install.py"}
NOT_SHIPPED_DIRS = ("tests", "__pycache__")
MD_BEGIN, MD_END = "<!-- context-system:begin -->", "<!-- context-system:end -->"
IGNORE_BEGIN, IGNORE_END = "# context-system:begin", "# context-system:end"
INDEX_SIGNATURE = "<!-- Built by tools/build_index.py"
BUILDER_SIGNATURE = "Rebuild index.md from the YAML headers"

AGENTS_POINTER = f"""
{MD_BEGIN}
## Context system

This repo keeps its memory in small files. Before anything else, read `CONTEXT.md` and
follow it: it says what to read at the start of a session and how to close one.
{MD_END}
"""


@dataclass(frozen=True)
class Step:
    action: str  # add, append, keep, clash
    path: str
    content: str = ""
    note: str = ""


def kit_files() -> list[str]:
    files = []
    for path in sorted(KIT.rglob("*")):
        rel = path.relative_to(KIT).as_posix()
        if path.is_dir() or rel in NOT_SHIPPED:
            continue
        if any(part in NOT_SHIPPED_DIRS for part in path.relative_to(KIT).parts):
            continue
        files.append(rel)
    return files


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_context_file(path: Path) -> bool:
    if path.name == ".gitkeep":
        return True
    try:
        return path.suffix == ".md" and read(path).startswith("---\n")
    except UnicodeDecodeError:
        return False


def plan_folders(target: Path) -> list[Step]:
    steps = []
    for name in CONTENT_DIRS:
        folder = target / name
        if not folder.exists():
            continue
        if not folder.is_dir():
            steps.append(Step("clash", f"{name}/", note="exists and is not a folder"))
            continue
        foreign = [p for p in folder.rglob("*") if p.is_file() and not is_context_file(p)]
        if foreign:
            names = ", ".join(p.relative_to(target).as_posix() for p in foreign[:3])
            steps.append(Step("clash", f"{name}/", note=f"already used for other files ({names})"))
    return steps


def plan_file(target: Path, rel: str, content: str) -> Step:
    dest = target / rel
    if not dest.exists():
        return Step("add", rel, content)
    current = read(dest)
    if current == content:
        return Step("keep", rel, note="already there")
    if rel.split("/")[0] in CONTENT_DIRS:
        return Step("keep", rel, note="yours, kept")
    if rel == "index.md" and INDEX_SIGNATURE in current:
        return Step("keep", rel, note="rebuilt after install")
    if rel == "tools/build_index.py" and BUILDER_SIGNATURE in current:
        return Step("keep", rel, note="a different version of the kit's; kept")
    if rel.startswith(".claude/skills/"):
        return Step("clash", rel, note="you have a skill of this name")
    return Step("clash", rel, note="exists and is not the kit's")


def plan_rules(target: Path) -> list[Step]:
    kit_rules = read(KIT / "AGENTS.md")
    agents, claude = target / "AGENTS.md", target / "CLAUDE.md"
    steps = []

    context_mode = agents.exists() and read(agents) != kit_rules
    if not agents.exists():
        steps.append(Step("add", "AGENTS.md", kit_rules))
    elif context_mode:
        steps.append(plan_file(target, "CONTEXT.md", kit_rules))
        if MD_BEGIN in read(agents):
            steps.append(Step("keep", "AGENTS.md", note="already points to CONTEXT.md"))
        else:
            steps.append(Step("append", "AGENTS.md", AGENTS_POINTER,
                              "your rules kept; a pointer to CONTEXT.md added at the end"))

    # Claude reads CLAUDE.md, so it imports the kit's rules by name: a pointer in prose
    # would leave loading them to the model's judgement.
    rules_file = "CONTEXT.md" if context_mode else "AGENTS.md"
    if not claude.exists():
        content = "@AGENTS.md\n@CONTEXT.md\n" if context_mode else "@AGENTS.md\n"
        steps.append(Step("add", "CLAUDE.md", content))
    else:
        text = read(claude)
        if MD_BEGIN in text or f"@{rules_file}" in text:
            steps.append(Step("keep", "CLAUDE.md", note="already imports the rules"))
        else:
            block = f"\n{MD_BEGIN}\n@{rules_file}\n{MD_END}\n"
            steps.append(Step("append", "CLAUDE.md", block,
                              f"your notes kept; an import of {rules_file} added at the end"))
    return steps


def plan_gitignore(target: Path) -> Step:
    kit_lines = read(KIT / ".gitignore")
    dest = target / ".gitignore"
    if not dest.exists():
        return Step("add", ".gitignore", kit_lines)
    current = read(dest)
    if IGNORE_BEGIN in current:
        return Step("keep", ".gitignore", note="already extended")
    have = {line.strip() for line in current.splitlines()}
    missing = [line for line in kit_lines.splitlines()
               if line.strip() and not line.startswith("#") and line.strip() not in have]
    if not missing:
        return Step("keep", ".gitignore", note="already covers the kit's lines")
    block = "\n".join(["", IGNORE_BEGIN, *missing, IGNORE_END, ""])
    return Step("append", ".gitignore", block, f"{len(missing)} line(s) added")


def make_plan(target: Path) -> list[Step]:
    steps = plan_folders(target)
    steps += plan_rules(target)
    steps += [plan_file(target, rel, read(KIT / rel)) for rel in kit_files()]
    steps.append(plan_gitignore(target))
    return steps


def apply(target: Path, steps: list[Step]) -> None:
    for step in steps:
        dest = target / step.path
        if step.action == "add":
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(step.content, encoding="utf-8")
        elif step.action == "append":
            current = read(dest)
            joiner = "" if current.endswith("\n") else "\n"
            dest.write_text(current + joiner + step.content, encoding="utf-8")


def show(steps: list[Step]) -> None:
    labels = {"add": "ADD   ", "append": "APPEND", "keep": "KEEP  ", "clash": "CLASH "}
    for step in steps:
        note = f"  ({step.note})" if step.note else ""
        print(f"  {labels[step.action]} {step.path}{note}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", type=Path, help="the repo to add the context system to")
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args(argv)

    target = args.target.resolve()
    if not target.is_dir():
        print(f"{target} is not a folder.")
        return 2
    if target == KIT:
        print("That is the kit itself; point this at your own repo.")
        return 2
    if not (target / ".git").exists():
        print("Note: this folder is not a git repo; the files will be added all the same.")

    steps = make_plan(target)
    clashes = [s for s in steps if s.action == "clash"]
    print(f"Plan for {target}:")
    show(steps)

    if clashes:
        print(f"\n{len(clashes)} clash(es). Nothing was written. Move or rename those, then run again.")
        return 1
    if not args.apply:
        print("\nDry run: nothing written. Run again with --apply to do it.")
        return 0

    apply(target, steps)
    built = subprocess.run([sys.executable, str(target / "tools" / "build_index.py")],
                           capture_output=True, text=True)
    print("\n" + built.stdout.strip())
    changed = [s.path for s in steps if s.action in ("add", "append")]
    print(f"\nDone: {len(changed)} file(s) added or extended. Commit them by name, then start a")
    print("session with your agent and type /start (or @start).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
