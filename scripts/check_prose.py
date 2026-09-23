#!/usr/bin/env python3
"""Prose gate: banned characters in every file this repository authors.

Two classes, both of which survive review because nobody sees them:

* the em dash (U+2014). The house style writes a hyphen or a comma. It
  arrives by copy-paste and by autocorrect, and once it sits in a comment
  block it is copied into the next repository with that block.
* characters that render as nothing: zero-width space, byte-order mark,
  soft hyphen, and the directional marks. They are legal text, they pass
  every structural check, and they break search and diffs silently.

Deliberately NOT flagged: the ellipsis, the en dash and the no-break space.
They are legitimate typography here, and a gate that fights legitimate
typography gets switched off.

``schema/`` is excluded because it is not authored here: it is a
byte-identical mirror of the pinned learn-content-engine release, held in
place by the drift gate. Its typography is the engine's to fix, and editing
it here would turn the drift gate red for a cosmetic reason.

Usage:
    python3 scripts/check_prose.py             # gate every tracked file
    python3 scripts/check_prose.py --self-test # prove the gate bites
"""
from __future__ import annotations

import subprocess
import sys
import unicodedata
from pathlib import Path

# Built from code points, never from literals: this file has to pass its own
# gate, and a table of the real characters would flag the gate itself.
BANNED = {
    chr(0x2014): "EM DASH (write a hyphen or a comma)",
    chr(0x200B): "ZERO WIDTH SPACE",
    chr(0xFEFF): "BYTE ORDER MARK",
    chr(0x00AD): "SOFT HYPHEN",
    chr(0x200E): "LEFT-TO-RIGHT MARK",
    chr(0x200F): "RIGHT-TO-LEFT MARK",
}

ALLOWED_SAMPLE = "a clean line - hyphen, comma, no-break space" + chr(0x00A0) + ", ellipsis" + chr(0x2026)

EXCLUDED_PREFIXES = ("schema/",)


def tracked_files() -> list[str]:
    """Every file git tracks, minus the mirrored artifacts."""
    listing = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.split("\n")
    return [
        path
        for path in listing
        if path and not path.startswith(EXCLUDED_PREFIXES)
    ]


def findings_in(text: str) -> list[tuple[int, str, str]]:
    """(line number, character, reason) for every banned character in ``text``."""
    findings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for character, reason in BANNED.items():
            if character in line:
                findings.append((line_number, character, reason))
    return findings


def describe(character: str) -> str:
    return f"U+{ord(character):04X} {unicodedata.name(character, 'UNNAMED')}"


def self_test() -> int:
    """A gate that never fires on a known-bad input is not a gate."""
    for character in BANNED:
        if not findings_in(f"a line with {character} in it"):
            print(f"self-test FAILED: {describe(character)} not detected", file=sys.stderr)
            return 1
    if findings_in("a clean line - hyphen, comma, no-break space , ellipsis…"):
        print("self-test FAILED: a clean line was flagged", file=sys.stderr)
        return 1
    print(f"self-test passed: {len(BANNED)} banned characters detected, clean text untouched")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()

    files = tracked_files()
    if not files:
        print("check_prose: git tracks no files - wrong directory?", file=sys.stderr)
        return 2

    hits = 0
    for path in files:
        try:
            text = Path(path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for line_number, character, reason in findings_in(text):
            hits += 1
            print(f"{path}:{line_number}: {describe(character)} - {reason}")

    if hits:
        print(f"\nPROSE GATE: {hits} banned character(s) in {len(files)} tracked file(s).", file=sys.stderr)
        return 1
    print(f"prose gate: {len(files)} tracked file(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
