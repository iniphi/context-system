"""The kit's own checks: the index builder, the header rules and the size caps."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parent.parent
SCRIPT = KIT / "tools" / "build_index.py"


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True, text=True,
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    dest = tmp_path / "repo"
    shutil.copytree(KIT, dest, ignore=shutil.ignore_patterns("tests", "__pycache__"))
    return dest


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_shipped_kit_passes_check() -> None:
    result = run(KIT, "--check")
    assert result.returncode == 0, result.stdout + result.stderr


def test_shipped_index_is_current(repo: Path) -> None:
    before = (repo / "index.md").read_text(encoding="utf-8")
    assert run(repo).returncode == 0
    assert (repo / "index.md").read_text(encoding="utf-8") == before


def test_index_lists_open_todos_by_priority_then_due(repo: Path) -> None:
    write(repo / "todo/2026-11-01-low.md",
          "---\ndescription: Low thing\nstatus: open\ncreated: 2026-11-01\npriority: low\n---\n")
    write(repo / "todo/2026-11-02-high-late.md",
          "---\ndescription: High late\nstatus: open\ncreated: 2026-11-02\npriority: high\ndue: 2026-12-01\n---\n")
    write(repo / "todo/2026-11-03-high-soon.md",
          "---\ndescription: High soon\nstatus: open\ncreated: 2026-11-03\npriority: high\ndue: 2026-11-20\n---\n")
    assert run(repo).returncode == 0
    index = (repo / "index.md").read_text(encoding="utf-8")
    order = [index.index(s) for s in ("High soon", "High late", "Low thing")]
    assert order == sorted(order)


def test_index_shows_only_recent_logs(repo: Path) -> None:
    for day in range(1, 16):
        write(repo / f"log/2026-10-{day:02d}-0900-s.md",
              f"---\ndate: 2026-10-{day:02d}\nsummary: Session {day}\n---\n")
    assert run(repo).returncode == 0
    index = (repo / "index.md").read_text(encoding="utf-8")
    assert "Session 15" in index and "Session 6" in index
    assert "Session 5:" not in index and "Session 5\n" not in index


def test_check_catches_missing_field(repo: Path) -> None:
    write(repo / "todo/2026-11-01-x.md", "---\ndescription: No status\ncreated: 2026-11-01\n---\n")
    result = run(repo, "--check")
    assert result.returncode == 1
    assert "status" in result.stdout


def test_check_catches_todo_in_wrong_folder(repo: Path) -> None:
    write(repo / "todo/2026-11-01-x.md",
          "---\ndescription: Done but not moved\nstatus: done\ncreated: 2026-11-01\nclosed: 2026-11-02\n---\n")
    assert run(repo, "--check").returncode == 1


def test_check_catches_oversized_state(repo: Path) -> None:
    state = repo / "context/state.md"
    state.write_text(state.read_text(encoding="utf-8") + "line\n" * 80, encoding="utf-8")
    result = run(repo, "--check")
    assert result.returncode == 1
    assert "state.md" in result.stdout


def test_check_catches_stale_index(repo: Path) -> None:
    write(repo / "decisions/2026-11-01-x.md",
          "---\ndescription: A new decision\ndate: 2026-11-01\n---\n")
    result = run(repo, "--check")
    assert result.returncode == 1
    assert "index.md" in result.stdout


def test_skill_headers_hold_only_name_and_description() -> None:
    skills = sorted((KIT / ".claude" / "skills").glob("*/SKILL.md"))
    assert {p.parent.name for p in skills} == {"start", "task", "close", "brainstorm"}
    for p in skills:
        head = p.read_text(encoding="utf-8").split("---")[1]
        keys = {line.split(":")[0] for line in head.strip().splitlines()}
        assert keys == {"name", "description"}, p
        assert f"name: {p.parent.name}" in head


def test_close_procedure_lives_only_in_the_skill() -> None:
    # Two copies of a procedure drift into conflicting instructions ("Skill Leakage",
    # dos Santos et al. 2026), so AGENTS.md points at the close skill instead.
    agents = (KIT / "AGENTS.md").read_text(encoding="utf-8")
    assert ".claude/skills/close/SKILL.md" in agents
    assert "build_index.py --check" not in agents


def test_claude_md_points_at_agents_md() -> None:
    assert (KIT / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"
