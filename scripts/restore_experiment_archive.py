"""Plan/restore numbered experiment code and assets from a historical ZIP.

This is deliberately conservative: it will not overwrite existing files and
defaults to a dry run. Verify the original archive hash manifest separately.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

from validate_experiment_archive import SLUGS


def destination(relative: Path) -> Path | None:
    """Map a legacy archival path to a numbered research directory.

    Parameters
    ----------
    relative : Path
        Relative pathname inside the historical repository ZIP.

    Returns
    -------
    Path or None
        Relative new destination path, or None when the file is unrelated.
    """
    parts = relative.parts
    if len(parts) < 2:
        return None
    for i, slug in enumerate(SLUGS, start=1):
        token = f"exp_{i:04d}"
        if parts[0] == "experiments":
            if parts[1] == f"run_{token}.py":
                return Path("proximity_isomap/code") / slug / "run.py"
            if parts[1] == f"EXP-{i:04d}.md":
                return Path("proximity_isomap/code") / slug / "HISTORICAL_PROTOCOL.md"
            if len(parts) > 2 and parts[1] == "configs" and token in parts[2]:
                return Path("proximity_isomap/code") / slug / "configs" / parts[2]
        if parts[0] == "results" and parts[1] == token:
            return Path("proximity_isomap/results") / slug / Path(*parts[2:])
        if parts[0] == "figures":
            if parts[1] == f"plot_{token}.py":
                return Path("proximity_isomap/code") / slug / "plot.py"
            if len(parts) > 3 and parts[1] == "experiments" and parts[2] == token:
                return Path("proximity_isomap/figures") / slug / Path(*parts[3:])
    return None


def plan_archive(archive: Path) -> list[tuple[str, Path]]:
    """List experiment assets and their proposed safe new paths.

    Parameters
    ----------
    archive : Path
        Historical cumulative research ZIP; no paths are written.

    Returns
    -------
    list[tuple[str, Path]]
        Archive member name and destination relative to the repository root.

    Notes
    -----
    Assumes all assets appear below an optional single repository prefix;
    excludes file names that could escape the intended root.
    """
    planned: list[tuple[str, Path]] = []
    with ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            path = Path(member.filename)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe archive path: {member.filename}")
            relative = path
            if relative.parts and relative.parts[0] == "ProximityGraphs-Isomap":
                relative = Path(*relative.parts[1:])
            target = destination(relative)
            if target is not None:
                planned.append((member.filename, target))
    return planned


def main() -> None:
    """Preview the migration or copy original ZIP bytes with explicit --apply."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    planned = plan_archive(args.archive)
    print(f"Found {len(planned)} historical files eligible for numbered folders.")
    if not args.apply:
        print("Dry run: no files written. Use --apply after inspecting the ZIP manifest.")
        return
    copied = 0
    with ZipFile(args.archive) as bundle:
        for member, relative in planned:
            target = args.repo / relative
            if target.exists():
                print(f"SKIP existing {relative}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(bundle.read(member))
            copied += 1
    print(f"Copied {copied} original files; verify hashes and rerun CI before committing.")


if __name__ == "__main__":
    main()
