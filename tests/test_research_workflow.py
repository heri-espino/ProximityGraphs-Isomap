"""Regression tests for paper registration and the PR handoff policy."""

import csv
from pathlib import Path

import pytest

from scripts.check_change_protocol import protocol_errors
from scripts.new_literature_entry import register
from scripts.validate_research import FIELDS, validate


def test_scaffold_research_integrity() -> None:
    assert validate() == []


def test_register_paper_without_inventing_source_or_result(tmp_path: Path) -> None:
    base = tmp_path / "literature"
    (base / "references").mkdir(parents=True)
    (base / "MANIFEST.csv").write_text(",".join(FIELDS) + "\n", encoding="utf-8")
    identifier = register("author2024topic", "A Paper on Geometry", 2024, root=tmp_path)
    assert identifier == "LIT-0001"
    with (base / "MANIFEST.csv").open(newline="", encoding="utf-8") as stream:
        record = list(csv.DictReader(stream))[0]
    assert record["review_status"] == "unreviewed"
    assert record["extraction_status"] == "pending"
    note = (base / "references/author2024topic.md").read_text(encoding="utf-8")
    assert "No result has been verified yet" in note
    with pytest.raises(ValueError, match="already registered"):
        register("author2024topic", "Duplicate", 2024, root=tmp_path)
    with pytest.raises(ValueError, match="key must"):
        register("../escape", "Unsafe", 2024, root=tmp_path)


def test_pr_workflow_requires_new_journal_and_synced_handoff() -> None:
    assert protocol_errors({"README.md"}, set()) == []
    errors = protocol_errors({"src/proximity_isomap/graphs/radius.py"}, set())
    assert len(errors) == 5
    changed = {
        "src/proximity_isomap/graphs/radius.py", "AI_HANDOFF.md", "journal/LATEST.md",
        "context/STATE.md", "context/NEXT_STEPS.md",
        "journal/2026-10/2026-10-16-scientific-change.md",
    }
    assert protocol_errors(changed, {"journal/2026-10/2026-10-16-scientific-change.md"}) == []
