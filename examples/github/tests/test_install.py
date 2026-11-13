"""The drop-in route: tools/install.py adds the kit to a repo that already exists."""
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parent.parent
INSTALL = KIT / "tools" / "install.py"
BEGIN = "<!-- context-system:begin -->"


def install(target: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(INSTALL), str(target), *args], capture_output=True, text=True,
    )


def check(target: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(target / "tools" / "build_index.py"), "--check"],
        capture_output=True, text=True,
    )


@pytest.fixture
def target(tmp_path: Path) -> Path:
    repo = tmp_path / "project"
    repo.mkdir()
    (repo / "main.py").write_text("print('hello')\n", encoding="utf-8")
    return repo


def test_dry_run_writes_nothing(target: Path) -> None:
    result = install(target)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--apply" in result.stdout
    assert sorted(p.name for p in target.iterdir()) == ["main.py"]


def test_bare_repo_gets_the_whole_kit(target: Path) -> None:
    result = install(target, "--apply")
    assert result.returncode == 0, result.stdout + result.stderr
    assert (target / "AGENTS.md").read_text(encoding="utf-8") == (KIT / "AGENTS.md").read_text(encoding="utf-8")
    assert (target / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"
    assert not (target / "CONTEXT.md").exists()
    for rel in ("context/state.md", "index.md", "tools/build_index.py",
                ".claude/skills/close/SKILL.md", "todo/.gitkeep"):
        assert (target / rel).exists(), rel
    assert not (target / "tools" / "install.py").exists()
    assert not (target / "tests").exists()
    assert check(target).returncode == 0


def test_existing_rule_files_are_kept_and_pointed(target: Path) -> None:
    (target / "AGENTS.md").write_text("# Our rules\n\nUse tabs.\n", encoding="utf-8")
    (target / "CLAUDE.md").write_text("# Claude notes\n\nBe brief.\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0

    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
    assert agents.startswith("# Our rules\n\nUse tabs.\n")
    assert claude.startswith("# Claude notes\n\nBe brief.\n")
    assert BEGIN in agents and "CONTEXT.md" in agents
    assert BEGIN in claude and "@CONTEXT.md" in claude
    assert (target / "CONTEXT.md").read_text(encoding="utf-8") == (KIT / "AGENTS.md").read_text(encoding="utf-8")
    assert check(target).returncode == 0


def test_claude_md_importing_their_agents_md_also_imports_context(target: Path) -> None:
    (target / "AGENTS.md").write_text("# Our rules\n", encoding="utf-8")
    (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
    assert claude.startswith("@AGENTS.md\n") and "@CONTEXT.md" in claude


def test_new_claude_md_imports_both_when_agents_md_is_theirs(target: Path) -> None:
    (target / "AGENTS.md").write_text("# Our rules\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n@CONTEXT.md\n"


def test_claude_md_already_importing_kit_agents_md_is_left_alone(target: Path) -> None:
    (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"


def test_only_claude_md_present(target: Path) -> None:
    (target / "CLAUDE.md").write_text("# Claude notes\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    assert (target / "AGENTS.md").read_text(encoding="utf-8") == (KIT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
    assert claude.startswith("# Claude notes\n") and "@AGENTS.md" in claude
    assert not (target / "CONTEXT.md").exists()


def test_second_run_changes_nothing(target: Path) -> None:
    (target / "AGENTS.md").write_text("# Our rules\n", encoding="utf-8")
    (target / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    before = {p: p.read_bytes() for p in target.rglob("*") if p.is_file()}
    result = install(target, "--apply")
    assert result.returncode == 0, result.stdout
    after = {p: p.read_bytes() for p in target.rglob("*") if p.is_file()}
    assert before == after
    assert (target / ".gitignore").read_text(encoding="utf-8").count("context-system:begin") == 1


def test_gitignore_is_extended_not_replaced(target: Path) -> None:
    (target / ".gitignore").write_text("node_modules/\n.env\n", encoding="utf-8")
    assert install(target, "--apply").returncode == 0
    text = (target / ".gitignore").read_text(encoding="utf-8")
    assert text.startswith("node_modules/\n.env\n")
    assert "__pycache__/" in text


def test_clash_in_a_folder_stops_everything(target: Path) -> None:
    (target / "log").mkdir()
    (target / "log" / "server.log").write_text("boot\n", encoding="utf-8")
    result = install(target, "--apply")
    assert result.returncode == 1
    assert "log/" in result.stdout
    assert not (target / "AGENTS.md").exists()
    assert not (target / "context").exists()


def test_clash_with_an_existing_skill_stops_everything(target: Path) -> None:
    skill = target / ".claude" / "skills" / "start" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("---\nname: start\ndescription: theirs\n---\n", encoding="utf-8")
    result = install(target, "--apply")
    assert result.returncode == 1
    assert "start" in result.stdout
    assert skill.read_text(encoding="utf-8").endswith("theirs\n---\n")
    assert not (target / "AGENTS.md").exists()


def test_missing_target_is_refused(tmp_path: Path) -> None:
    result = install(tmp_path / "nowhere", "--apply")
    assert result.returncode == 2
