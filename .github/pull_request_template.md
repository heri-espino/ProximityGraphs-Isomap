## Summary

What changed and why? Link the mathematical definitions, source-backed literature result IDs, or experiment protocols affected by this change.

## Research continuity checklist

- [ ] Read the journal's latest dated entry **before** changing code or research notes.
- [ ] Created a new dated, append-only journal entry for substantive work, including failures and tested commands.
- [ ] Updated `journal/LATEST.md`, `AI_HANDOFF.md`, `context/STATE.md` and `context/NEXT_STEPS.md`.
- [ ] Added or updated NumPy-style source docstrings, unit tests and Sphinx-generated API documentation if code changed.
- [ ] Registered any new papers in `literature/MANIFEST.csv`; recorded source PDF, Docling Markdown, exact-result locators and verification status.
- [ ] Registered experiment configurations and retained negative findings where relevant.
- [ ] Ran `python -m pytest`, Ruff, `scripts/validate_research.py` and Sphinx, or documented unavailable checks.

## Limitations and remaining open questions

Explicitly identify proposals, unverified mathematical claims and any unavailable evidence.
