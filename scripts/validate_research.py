"""Check navigability, source-paper provenance and basic Sphinx docstring hygiene.

The checks validate *structure*, not the correctness of a proof, citation,
mathematical conclusion, or AI's actual compliance with reading instructions.
"""

import ast
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "paper_id", "citation_key", "title", "year", "doi", "pdf_path", "markdown_path",
    "reference_path", "extraction_status", "review_status",
)
EXTRACTION_STATES = {"pending", "pdf_only", "extracted"}
REVIEW_STATES = {"unreviewed", "in_progress", "reviewed"}


def validate(root: Path = ROOT) -> list[str]:
    """Return actionable integrity errors for the research repository.

    Parameters
    ----------
    root : pathlib.Path
        Root directory containing the research scaffold.

    Returns
    -------
    list[str]
        Error messages; an empty list indicates structural checks passed.

    Notes
    -----
    Verifies required files, latest-journal pointers, literature registration and
    basic public API docstrings. Does not assess scientific or bibliographic truth.
    """
    errors: list[str] = []
    required = (
        "AGENTS.md", "AI_HANDOFF.md", "README.md", "environment.yml",
        "proximity_isomap/history/journal/README.md",
        "proximity_isomap/history/journal/LATEST.md",
        "proximity_isomap/history/context/STATE.md",
        "proximity_isomap/history/context/NEXT_STEPS.md",
        "proximity_isomap/history/context/DECISION_INDEX.md",
        "literature/README.md", "literature/MANIFEST.csv",
        "literature/pdf", "literature/markdown", "literature/references",
        "literature/references/PAPER_TEMPLATE.md", "literature/references/KEY_RESULTS.md",
        "literature/references/library.bib", "docs/api.rst",
    )
    for name in required:
        if not (root / name).exists():
            errors.append(f"missing required path: {name}")
    if errors:
        return errors

    latest = (root / "proximity_isomap/history/journal/LATEST.md").read_text(encoding="utf-8")
    handoff = (root / "AI_HANDOFF.md").read_text(encoding="utf-8")
    match = re.search(r"\]\((\d{4}-\d\d/\d{4}-\d\d-\d\d-[^)]+\.md)\)", latest)
    if not match:
        errors.append("journal/LATEST.md must link a YYYY-MM/YYYY-MM-DD-topic.md entry")
    else:
        target = Path("proximity_isomap/history/journal") / match.group(1)
        if not (root / target).is_file():
            errors.append(f"latest journal target absent: {target}")
        if target.as_posix() not in handoff:
            errors.append("AI_HANDOFF.md must link the current latest journal entry")

    manifest_path = root / "literature/MANIFEST.csv"
    with manifest_path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            errors.append("literature/MANIFEST.csv columns must match the documented schema")
            rows = []
        else:
            rows = list(reader)
    seen_keys: set[str] = set()
    seen_ids: set[str] = set()
    registered_files: set[str] = set()
    for line_no, row in enumerate(rows, start=2):
        key = row["citation_key"]
        paper_id = row["paper_id"]
        prefix = f"literature/MANIFEST.csv:{line_no} ({key})"
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key):
            errors.append(f"{prefix}: unsafe citation key")
            continue
        if not re.fullmatch(r"LIT-\d{4}", paper_id):
            errors.append(f"{prefix}: invalid stable paper ID")
        if key.lower() in seen_keys or paper_id in seen_ids:
            errors.append(f"{prefix}: duplicate citation key or paper ID")
        seen_keys.add(key.lower())
        seen_ids.add(paper_id)
        if row["extraction_status"] not in EXTRACTION_STATES:
            errors.append(f"{prefix}: unrecognized extraction_status")
        if row["review_status"] not in REVIEW_STATES:
            errors.append(f"{prefix}: unrecognized review_status")
        if not row["title"].strip() or not re.fullmatch(r"\d{4}", row["year"]):
            errors.append(f"{prefix}: title or publication year missing")
        path_names = {
            "pdf_path": f"pdf/{key}.pdf",
            "markdown_path": f"markdown/{key}.md",
            "reference_path": f"references/{key}.md",
        }
        for field, expected in path_names.items():
            if row[field] != expected:
                errors.append(f"{prefix}: {field} must be {expected}")
        registered_files.update([row["pdf_path"], row["markdown_path"]])
        pdf = root / "literature" / path_names["pdf_path"]
        md = root / "literature" / path_names["markdown_path"]
        note = root / "literature" / path_names["reference_path"]
        if not note.is_file():
            errors.append(f"{prefix}: missing annotation {note.relative_to(root)}")
        stage = row["extraction_status"]
        if stage == "pending" and (pdf.exists() or md.exists()):
            errors.append(f"{prefix}: update extraction_status after adding files")
        if stage == "pdf_only" and (not pdf.exists() or md.exists()):
            errors.append(f"{prefix}: pdf_only requires a PDF but no extracted Markdown")
        if stage == "extracted" and not (pdf.exists() and md.exists()):
            errors.append(f"{prefix}: extracted but PDF or Markdown is missing")
        if row["review_status"] == "reviewed":
            if row["extraction_status"] != "extracted":
                errors.append(f"{prefix}: reviewed paper must have extracted PDF and Markdown")
            if note.is_file():
                content = note.read_text(encoding="utf-8")
                if not re.search(rf"{re.escape(paper_id)}-R\d{{2}}", content):
                    errors.append(f"{prefix}: reviewed paper has no local result identifiers")

    for subdir, extension in (("pdf", "pdf"), ("markdown", "md")):
        for file in (root / "literature" / subdir).glob(f"*.{extension}"):
            relative = f"{subdir}/{file.name}"
            if relative not in registered_files:
                errors.append(f"unregistered literature source: literature/{relative}")

    api_root = root / "src/proximity_isomap"
    if api_root.exists():
        for source in api_root.rglob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
            if not ast.get_docstring(tree):
                errors.append(f"missing module docstring: {source.relative_to(root)}")
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name.startswith("_"):
                        continue
                    doc = ast.get_docstring(node)
                    if not doc:
                        errors.append(
                            f"missing public docstring: {source.relative_to(root)}:{node.lineno}"
                        )
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and doc:
                        if "Parameters\n----------" not in doc:
                            errors.append(
                                "public function lacks NumPy Parameters section: "
                                f"{source.relative_to(root)}:{node.lineno}"
                            )
                        if "Returns\n-------" not in doc:
                            errors.append(
                                "public function lacks NumPy Returns section: "
                                f"{source.relative_to(root)}:{node.lineno}"
                            )
    return errors


def main() -> None:
    """Print checks and exit nonzero on structural research-integrity failures."""
    problems = validate()
    if problems:
        for issue in problems:
            print("ERROR:", issue)
        raise SystemExit(1)
    print("Research documentation, literature manifest and API docstring checks: PASS")


if __name__ == "__main__":
    main()
