"""Rebuild index.md from the YAML headers of the context files, or check them.

    python tools/build_index.py           rebuild index.md
    python tools/build_index.py --check   report problems, change nothing (exit 1 if any)

Standard library only, so it runs on any laptop with Python 3.10 or later.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

RECENT_LOGS = 10
PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}

# Fields every file in a folder must carry in its header.
REQUIRED = {
    "context": ("description", "updated"),
    "log": ("date", "summary"),
    "todo": ("description", "status", "created"),
    "done": ("description", "status", "created", "closed"),
    "decisions": ("description", "date"),
}

# What an agent reads at the start of every session, and the most each may hold.
LINE_CAPS = {"AGENTS.md": 150, "CONTEXT.md": 150, "context/state.md": 60, "index.md": 120}
STARTUP_BYTES_CAP = 32 * 1024  # Codex truncates context files past this, silently


@dataclass(frozen=True)
class Entry:
    path: str
    fields: dict[str, str]

    def get(self, key: str, default: str = "") -> str:
        return self.fields.get(key, default)


def read_header(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def collect(root: Path) -> tuple[dict[str, list[Entry]], list[str]]:
    folders: dict[str, list[Entry]] = {name: [] for name in REQUIRED}
    problems: list[str] = []
    for name, required in REQUIRED.items():
        for path in sorted((root / name).glob("*.md")):
            rel = path.relative_to(root).as_posix()
            fields = read_header(path)
            if fields is None:
                problems.append(f"{rel}: no YAML header (--- lines at the top)")
                continue
            missing = [f for f in required if not fields.get(f)]
            if missing:
                problems.append(f"{rel}: header lacks {', '.join(missing)}")
            if name == "todo" and fields.get("status") not in (None, "", "open"):
                problems.append(f"{rel}: status is {fields['status']}; a closed to-do moves to done/")
            if name == "todo" and fields.get("priority", "normal") not in PRIORITY_ORDER:
                problems.append(f"{rel}: priority must be high, normal or low")
            if name == "done" and fields.get("status") not in (None, "", "done"):
                problems.append(f"{rel}: in done/ but status is {fields['status']}")
            folders[name].append(Entry(rel, fields))
    return folders, problems


def todo_key(entry: Entry) -> tuple:
    return (
        PRIORITY_ORDER.get(entry.get("priority", "normal"), 1),
        entry.get("due") or "9999",
        entry.get("created"),
    )


def render(folders: dict[str, list[Entry]]) -> str:
    out = [
        "# Index",
        "",
        "<!-- Built by tools/build_index.py from each file's header: change the file, then",
        "     rebuild. A chat with no shell may edit lines here by hand; the next rebuild",
        "     replaces them. -->",
        "",
        "## Context",
        "",
    ]
    out += [f"- [{e.path}]({e.path}) - {e.get('description')} (updated {e.get('updated')})"
            for e in folders["context"]]

    out += ["", "## Open to-dos", ""]
    todos = sorted(folders["todo"], key=todo_key)
    for e in todos:
        extra = [e.get("priority", "normal")]
        if e.get("due"):
            extra.append(f"due {e.get('due')}")
        out.append(f"- [{e.path}]({e.path}) - {e.get('description')} ({', '.join(extra)})")
    if not todos:
        out.append("- none")

    out += ["", "## Decisions", ""]
    decisions = sorted(folders["decisions"], key=lambda e: e.get("date"), reverse=True)
    out += [f"- {e.get('date')} [{e.path}]({e.path}) - {e.get('description')}" for e in decisions]
    if not decisions:
        out.append("- none yet")

    out += ["", f"## Recent sessions (newest {RECENT_LOGS})", ""]
    logs = sorted(folders["log"], key=lambda e: e.path, reverse=True)
    out += [f"- {e.get('date')} [{e.path}]({e.path}) - {e.get('summary')}"
            for e in logs[:RECENT_LOGS]]
    if not logs:
        out.append("- none yet")
    if len(logs) > RECENT_LOGS:
        out.append(f"- {len(logs) - RECENT_LOGS} older sessions in log/")

    out += ["", f"Done: {len(folders['done'])} to-dos in done/.", ""]
    return "\n".join(out)


def check_caps(root: Path) -> list[str]:
    problems = []
    for rel, cap in LINE_CAPS.items():
        path = root / rel
        if path.exists():
            lines = len(path.read_text(encoding="utf-8").splitlines())
            if lines > cap:
                problems.append(f"{rel}: {lines} lines, cap is {cap}")
    startup = [root / rel for rel in LINE_CAPS]
    logs = sorted((root / "log").glob("*.md"))
    if logs:
        startup.append(logs[-1])
    size = sum(p.stat().st_size for p in startup if p.exists())
    if size > STARTUP_BYTES_CAP:
        problems.append(f"start-up load is {size} bytes, cap is {STARTUP_BYTES_CAP}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report problems, change nothing")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)

    folders, problems = collect(args.root)
    index_path = args.root / "index.md"
    built = render(folders)

    if args.check:
        current = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
        if current != built:
            problems.append("index.md: out of date; run python tools/build_index.py")
        problems += check_caps(args.root)
        for p in problems:
            print(f"PROBLEM {p}")
        print("OK" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0

    index_path.write_text(built, encoding="utf-8")
    for p in problems:
        print(f"PROBLEM {p}")
    print(f"index.md rebuilt ({len(built.splitlines())} lines)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
