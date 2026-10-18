"""Structural safeguards for all nine canonical research records."""

from pathlib import Path

from scripts.validate_experiment_archive import ARCHIVE, SLUGS, validate


def test_every_experiment_has_matching_folders() -> None:
    """Require a synchronized four-folder home for every registered experiment."""
    assert len(SLUGS) == 9
    assert validate() == []
    for slug in SLUGS:
        for part in ("notes", "code", "figures", "results"):
            assert (ARCHIVE / part / slug / "README.md").exists()


def test_reports_missing_summary_figure(tmp_path: Path) -> None:
    """Ensure archive validation detects missing records rather than hiding them."""
    errors = validate(tmp_path)
    assert errors
    assert any("missing experiment artifact" in error for error in errors)


def test_all_experiment_notes_include_mathematics_and_figure_plans() -> None:
    """Require math and a non-broken figure plan before running full experiments."""
    for slug in SLUGS:
        content = (ARCHIVE / "notes" / slug / "README.md").read_text(encoding="utf-8")
        assert "## Mathematics:" in content
        assert "$$" in content
        assert "## Figure plan and reproduction status" in content
