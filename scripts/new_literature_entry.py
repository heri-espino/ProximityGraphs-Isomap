"""Register a paper without fabricating PDF ingestion or mathematical results.

The resulting annotation is a to-do template. Review statuses are never
silently upgraded by the registration step.
"""

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "literature/MANIFEST.csv"
KEY_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")


def register(key: str, title: str, year: int, doi: str = "", root: Path = ROOT) -> str:
    """Create a unique manifest row and empty source-verification annotation.

    Parameters
    ----------
    key : str
        Unique ASCII citation key used for filenames and BibTeX.
    title : str
        Bibliographic title (not extracted from a source).
    year : int
        Four-digit publication year.
    doi : str
        Optional DOI provided by the researcher.
    root : pathlib.Path
        Repository root; overridable for automated tests.

    Returns
    -------
    str
        Stable `LIT-####` record identifier.

    Raises
    ------
    ValueError
        If metadata is invalid or the paper is already registered.
    FileExistsError
        If the target annotation exists outside the manifest.
    """
    if not KEY_PATTERN.fullmatch(key):
        raise ValueError(
            "key must start with a letter and contain only ASCII letters, digits, _ or -"
        )
    if not title.strip() or not 1500 <= year <= 2100:
        raise ValueError("title must be nonempty and year must be between 1500 and 2100")

    base = root / "literature"
    catalog = base / "MANIFEST.csv"
    with catalog.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if any(row["citation_key"].lower() == key.lower() for row in rows):
        raise ValueError(f"citation key {key!r} already registered")

    next_id = 1 + max([int(row["paper_id"].split("-")[1]) for row in rows], default=0)
    paper_id = f"LIT-{next_id:04d}"
    annotation = base / "references" / f"{key}.md"
    if annotation.exists():
        raise FileExistsError(annotation)

    content = f"""# {title} — {key}

**Paper ID:** `{paper_id}`  
**Citation key:** `{key}`  
**Authors / year:** authors TBD / {year}  
**DOI / canonical URL:** {doi or 'TBD'}  
**Primary PDF:** `../pdf/{key}.pdf`  
**Docling Markdown:** `../markdown/{key}.md`  
**Docling version / command / date:** TBD  
**Review status:** `unreviewed`  
**Reviewer / verified date:** TBD

## 1. Research question and contribution

TBD — examine the original source.

## 2. Assumptions and notation

TBD — verify all hypotheses and symbols in the original PDF.

## 3. Key results (one block per result)

Create `### {paper_id}-R01 — title` with type, exact PDF page and theorem/equation,
verified statement, proof idea, assumptions, limitations and relevance.
**No result has been verified yet.**

## 4. Algorithms and empirical setup

TBD.

## 5. Novelty matrix / relationship to our work

TBD — identify overlap with connected/disconnected Isomap and hybrid MDS.

## 6. Extraction and verification warnings

TBD — note Docling version and PDF-versus-Markdown discrepancies.

## 7. Follow-up questions

TBD.
"""
    entry = {
        "paper_id": paper_id,
        "citation_key": key,
        "title": title.strip(),
        "year": str(year),
        "doi": doi.strip(),
        "pdf_path": f"pdf/{key}.pdf",
        "markdown_path": f"markdown/{key}.md",
        "reference_path": f"references/{key}.md",
        "extraction_status": "pending",
        "review_status": "unreviewed",
    }
    annotation.write_text(content, encoding="utf-8")
    with catalog.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(entry))
        writer.writerow(entry)
    return paper_id


def main() -> None:
    """Read CLI metadata and register an explicitly unreviewed paper."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--doi", default="")
    args = parser.parse_args()
    print(register(args.key, args.title, args.year, args.doi))


if __name__ == "__main__":
    main()
