#!/usr/bin/env python3
"""The template ships only hidden example sets (#42).

This test belongs to the template alone (a ``repo`` row in
``.github/ownership.json``): a content repository created from the template
replaces the example with its own sets, which it wants visible. It lives in
its own file so the search index tests, which the hub owns and every
repository copies, stay the same everywhere.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_search_index as gsi  # noqa: E402


def test_shipped_example_sets_are_hidden() -> None:
    """Every set this TEMPLATE ships is a hidden example (#42).

    A template is copied, not shipped: whatever visibility the example
    carries is inherited by every repository created from it. A visible
    example means an author registers their new repo and advertises a
    demo set as their first content - and does not notice, because the
    list looks filled. Nothing between here and the learner's Discover
    list catches it: ``validate_registered_repo.py`` checks clone,
    commit, schema and repo slug but says nothing about the content, and
    ``visible`` is the app's normal case. The sibling test repository
    already ships its demo set hidden; this pins the same for the
    template.

    Deliberately shipping a visible set means deleting one line here and
    one in the manifest - a conscious act, which is the point.
    """
    index, build_errors = gsi.build_index()
    assert not build_errors
    assert index["sets"], "index carries no sets"
    for entry in index["sets"]:
        assert entry["visibility"] == "hidden", (
            f"set {entry['id']!r} is advertised as visible; a repository "
            "created from this template would inherit that"
        )
