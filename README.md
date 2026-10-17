# ProximityGraphs-Isomap

**Research status: exploratory.** An installable Python research baseline for proximity graphs, disconnected graph geodesics and manifold dimensionality reduction. No novel algorithm or superiority claim has been established.

## AI and research continuity — start here

1. **[`AGENTS.md`](AGENTS.md)** — required reading and end-of-session documentation rules.
2. **[`journal/README.md`](journal/README.md)**, **[`journal/LATEST.md`](journal/LATEST.md)** and the linked dated entry — read **first**, before summaries.
3. **[`AI_HANDOFF.md`](AI_HANDOFF.md)** — compact current handoff, work completed and unresolved issues.
4. **[`context/STATE.md`](context/STATE.md)**, **[`context/NEXT_STEPS.md`](context/NEXT_STEPS.md)** — authoritative state and prioritized follow-ups.

Every substantive change requires a new dated journal entry, an updated `journal/LATEST.md` pointer and an updated AI handoff. Test/code updates require Sphinx-compatible NumPy-style docstrings. CI checks structural consistency (not mathematical truth).

## Research directories

| Location | Role |
| --- | --- |
| `src/proximity_isomap/` | Reusable Python library, with API docstrings |
| `tests/` | Unit tests and numerical behavior checks |
| `notes/` | Mathematical notebook: definitions, propositions, proofs and conjectures (Obsidian-compatible) |
| `journal/` | Append-only reasoning chronology and architectural decisions |
| [`literature/`](literature/README.md) | **`pdf/` original papers, `markdown/` Docling extractions, `references/` source-checked results and BibTeX** |
| `experiments/`, `results/` | Registered configurations and reproducible scientific evidence |
| `figures/` | Plot source and selected manuscript images |
| `paper/` | LaTeX manuscript skeleton using `literature/references/library.bib` |
| `docs/` | Sphinx technical and research-workflow documentation |
| `scripts/` | Literature registration and research-integrity checks |

## Installation and checks (Python 3.11+)

```bash
python -m venv .venv
# Activate the environment (PowerShell: .venv\Scripts\Activate.ps1)
python -m pip install -e ".[dev,docs]"
python -m pytest -q
python -m ruff check src tests examples experiments scripts
python scripts/validate_research.py
python -m sphinx -b html -W docs docs/_build/html
```

Run a simple sample or a preregistered exploratory experiment:

```bash
python examples/radius_graph_basics.py
python experiments/run_exp_0001.py --config experiments/configs/exp_0001.json
```

Results are exploratory, not independent evidence of an improved algorithm.

## Literature ingestion example

```bash
python scripts/new_literature_entry.py --key author2024topic --title "Article title" --year 2024
# Add the source PDF under literature/pdf/author2024topic.pdf
# Then use Docling to write literature/markdown/author2024topic.md
# Verify results against the original PDF; annotate literature/references/author2024topic.md
python scripts/validate_research.py
```

See [`literature/README.md`](literature/README.md) for the complete procedure and `KEY_RESULTS.md` for the verified cross-paper result index. Nothing should be marked `reviewed` solely from an automated extraction.

## Current scientific idea

For samples `X = {x_1, ..., x_n}`, build an undirected radius graph with `(i,j)` iff `||x_i-x_j|| <= r`, with Euclidean edge weights. Within connected components, estimate graph geodesics; across different components, consider ambient Euclidean dissimilarities or rigid alignment. Compare full weighted-stress optimization, rigidly aligned component embeddings, classical MDS/PCA and standard Isomap under identical test sets.

These are existing building blocks. The contribution, if any, requires verified new theory, a method with a clear distinction from prior work, or robust experimental findings. In folded manifolds Euclidean cross-component distances can be misleading.

## License

**Not selected yet.** Do not assume this repository grants permission to redistribute code or third-party literature PDFs. Only import papers when storage and sharing are permitted.
