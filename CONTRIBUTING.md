# Contributing and reproducibility

**Start by reading `AGENTS.md`, then the journal (`journal/README.md`, `journal/LATEST.md` and its linked entry), and only then the AI handoff and current context.** This order applies to AI assistants as well as human collaborators.

For source changes, add type hints, NumPy-style docstrings (Parameters, Returns, Notes/References when relevant), tests, and Sphinx autodoc coverage. For proof/experiment/literature changes, retain exact assumptions, stable IDs, source links, configuration, environments and negative results. Never turn a Docling extraction into an unverified theorem or label a proposal established.

Before completion:

```bash
python -m pytest -q
python -m ruff check src tests examples experiments scripts
python scripts/validate_research.py
python -m sphinx -b html -W docs docs/_build/html
```

Then append a dated journal entry, update `journal/LATEST.md`, `AI_HANDOFF.md`, `context/STATE.md` and `context/NEXT_STEPS.md`, and register any new ADR/literature source/experiment. Automated checks cover only structural rules; source verification and mathematical claims require substantive review.
