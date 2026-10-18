"""Require dated research breadcrumbs when a PR changes scientific artifacts.

This is an optional strict CI policy: it applies to proposed changes compared
with a base Git revision and cannot verify whether an AI actually read files.
"""

import argparse
import re
import subprocess
from pathlib import Path

JOURNAL_ENTRY_PATTERN = re.compile(r"journal/\d{4}-\d{2}/\d{4}-\d{2}-\d{2}-[\w-]+\.md$")
RESEARCH_PREFIXES = (
    "src/", "tests/", "notes/", "literature/", "experiments/", "results/",
    "paper/", "figures/", "docs/", "scripts/", "proximity_isomap/",
)
REQUIRED_UPDATES = (
    "AI_HANDOFF.md", "journal/LATEST.md", "context/STATE.md", "context/NEXT_STEPS.md",
)


def protocol_errors(changed: set[str], added: set[str]) -> list[str]:
    """List missing handoff changes for a set of revised research files.

    Parameters
    ----------
    changed : set[str]
        Paths modified or introduced compared with the PR's base commit.
    added : set[str]
        Paths added, excluding previously existing journal entries.

    Returns
    -------
    list[str]
        Requirements not met by a substantive source/research change.
    """
    substantive = any(name.startswith(RESEARCH_PREFIXES) for name in changed)
    if not substantive:
        return []
    errors = [f"required synchronized update absent: {name}" for name in REQUIRED_UPDATES
              if name not in changed]
    if not any(JOURNAL_ENTRY_PATTERN.fullmatch(name) for name in added):
        errors.append("a new dated journal/YYYY-MM/YYYY-MM-DD-topic.md entry is required")
    return errors


def main() -> None:
    """Check repository changes against a Git base revision for CI pull requests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Git base ref, e.g. origin/main")
    base = parser.parse_args().base
    root = Path(__file__).resolve().parents[1]
    common = ["git", "-C", str(root), "diff", "--name-only"]
    changes = subprocess.check_output(common + [f"{base}...HEAD"], text=True).splitlines()
    additions = subprocess.check_output(
        common + ["--diff-filter=A", f"{base}...HEAD"], text=True
    ).splitlines()
    errors = protocol_errors(set(changes), set(additions))
    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)
    print("Pull-request research documentation handoff policy: PASS")


if __name__ == "__main__":
    main()
