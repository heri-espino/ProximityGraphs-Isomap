"""Validate numbered experiment research records and their local Markdown links.

This is a structural integrity check; it does not validate numerical claims,
recover absent historical source, or prove that plots match their archived runs.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "proximity_isomap"

SLUGS = (
    "001-radius_filtration",
    "002-hybrid_mds",
    "003-wide_radius_grid",
    "004-radius_transfer",
    "005-paired_manifolds",
    "006-rotated_swiss_rolls",
    "007-component_alignment",
    "008-multiple_swiss_rolls",
    "009-topological_manifolds",
)
LINK_PATTERN = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")


def validate(root: Path = ROOT) -> list[str]:
    """Return missing-artifact and invalid-relative-link errors.

    Parameters
    ----------
    root : Path
        Root of the repository containing the `proximity_isomap/` archive.

    Returns
    -------
    list[str]
        Empty when every numbered experiment has code/notes/figures/results
        directories and their required documentation/summary diagram.
    """
    errors: list[str] = []
    folder = root / "proximity_isomap"
    required = ("README.md", "MANIFEST.json", "notes/README.md", "code/README.md",
                "figures/README.md", "results/README.md")
    for name in required:
        if not (folder / name).is_file():
            errors.append(f"missing research archive root path: {name}")
    for slug in SLUGS:
        for sub, expected in (
            ("notes", "README.md"), ("code", "README.md"),
            ("figures", "README.md"), ("figures", "summary.svg"),
            ("results", "README.md"),
        ):
            candidate = folder / sub / slug / expected
            if not candidate.is_file():
                errors.append(f"missing experiment artifact: {candidate.relative_to(root)}")
        note = folder / "notes" / slug / "README.md"
        if not note.exists():
            continue
        content = note.read_text(encoding="utf-8")
        if "## Mathematics:" not in content:
            errors.append(f"experiment mathematics missing: {note.relative_to(root)}")
        if "## Figure plan and reproduction status" not in content:
            errors.append(f"experiment figure plan missing: {note.relative_to(root)}")
        for href in LINK_PATTERN.findall(content):
            if "://" in href or href.startswith("#"):
                continue
            target = (note.parent / href).resolve()
            if not target.is_file():
                errors.append(f"broken experiment note link: {note.relative_to(root)} -> {href}")
    return errors


def main() -> None:
    """Run the experiment-archive integrity check from a clean checkout."""
    errors = validate()
    if errors:
        for problem in errors:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("Numbered experiment notes, code ledgers, figures and results: PASS")


if __name__ == "__main__":
    main()
