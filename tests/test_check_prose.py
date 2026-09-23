"""Unit tests for the prose gate (scripts/check_prose.py).

The gate's own ``--self-test`` proves it fires on every banned character;
these tests pin the behaviour that a reader would otherwise have to trust:
which characters are banned, which legitimate typography stays untouched,
and that the mirrored schema/ tree is out of scope by construction.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_prose", REPO_ROOT / "scripts" / "check_prose.py"
)
check_prose = importlib.util.module_from_spec(SPEC)
sys.modules["check_prose"] = check_prose
SPEC.loader.exec_module(check_prose)


EM_DASH = chr(0x2014)
ZERO_WIDTH_SPACE = chr(0x200B)
ELLIPSIS = chr(0x2026)
EN_DASH = chr(0x2013)
NO_BREAK_SPACE = chr(0x00A0)


def test_flags_an_em_dash():
    findings = check_prose.findings_in(f"a comment {EM_DASH} with an em dash")
    assert [f[1] for f in findings] == [EM_DASH]
    assert findings[0][0] == 1


def test_flags_an_invisible_character():
    assert check_prose.findings_in(f"zero{ZERO_WIDTH_SPACE}width")


def test_leaves_legitimate_typography_alone():
    # Ellipsis, en dash and no-break space are deliberately not banned: a
    # gate that fights legitimate typography gets switched off.
    assert check_prose.findings_in(f"one{ELLIPSIS}twelve, 5{EN_DASH}10, 12{NO_BREAK_SPACE}h") == []


def test_reports_the_line_number():
    findings = check_prose.findings_in(f"clean\nstill clean\nnow {EM_DASH} here")
    assert findings[0][0] == 3


def test_excludes_the_mirrored_schema_tree():
    # schema/ is a byte-identical mirror of the pinned engine release; its
    # typography belongs to the engine, and editing it here would turn the
    # drift gate red.
    assert any(path.startswith("schema/") for path in _all_git_files())
    assert not any(path.startswith("schema/") for path in check_prose.tracked_files())


def test_self_test_passes():
    assert check_prose.self_test() == 0


def _all_git_files() -> list[str]:
    import subprocess

    return subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True, cwd=REPO_ROOT
    ).stdout.split()
