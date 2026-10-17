# Getting started

Before contributing, follow the entrypoints in `AGENTS.md`: **read the latest journal first**, then `AI_HANDOFF.md`, then the current context summaries.

From the repository root:

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest -q
python -m ruff check src tests examples experiments scripts
python scripts/validate_research.py
python examples/radius_graph_basics.py
python -m sphinx -b html -W docs docs/_build/html
```

The current package builds a radius graph, computes finite hybrid dissimilarities and evaluates normalized within-/between-component stress. It does not yet fit a hybrid embedding.

Use the literature workflow in `docs/literature.md` to register original PDFs, Docling-extracted Markdown, and page-verified paper results without inventing mathematical claims.
