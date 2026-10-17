# 2026-10-16 — AI workflow and literature architecture

**Status:** scaffold/documentation improvement. **No scientific result is claimed.**

## Question / objective

How can an AI assistant resume research reliably with limited context, document its software and mathematics continuously, and link PDF research sources to verified theorem/algorithm summaries?

## Decisions and rationale

- The repository starts with the **chronological journal**. Agents read `journal/README.md`, `journal/LATEST.md`, and its linked dated entry before handoff and current state. This preserves reasoning and prevents a stale summary from being treated as the whole history.
- `AGENTS.md` specifies workflow; `AI_HANDOFF.md` preserves current session context; `context/` preserves canonical state and plans. Each serves a different role.
- `literature/pdf/` contains original papers; `literature/markdown/` contains Docling-derived conversions; `literature/references/` contains per-paper annotations, a cross-paper key-results index and the canonical `.bib` database.
- Literature conversion is **not** mathematical verification. Exact results must be checked against primary PDF pages/theorems before use in proofs or manuscript claims.
- CI validates navigation, per-paper records and basic public-API docstrings. Semantic research quality remains a human/AI review responsibility.

## Changed files

`AGENTS.md`, `AI_HANDOFF.md`, `README.md`, `CONTRIBUTING.md`, `journal/LATEST.md`, `journal/README.md`, `context/*`, `literature/`, `notes/literature/README.md`, `paper/`, `docs/`, `scripts/`, `.github/workflows/ci.yml` and public API docstrings where needed.

## Alternatives considered

- Storing everything only in a diary: chronological, but too expensive to read for each new session.
- Storing everything only in an AI summary: convenient but loses reasons, revisions and evidence.
- One directory mixing PDFs, extracted text and annotated results: harder to identify the authoritative source and conversion provenance.

## Verification

Automated tests, linting, Sphinx build, and research-file checks are part of scaffold verification. Exact results should be recorded here only after execution; until then do not infer success from the existence of CI configuration.

## Open questions / limitations

- Machine checks cannot force every external AI product to read files, follow semantic documentation policy, or write correct proofs.
- No PDFs have been imported or independently reviewed yet.
- The literature review must address existing Isomap, metric MDS, disconnected graphs, manifold alignment, and random geometric graph results before any novelty claim.

## Next actions

Follow [`../../context/NEXT_STEPS.md`](../../context/NEXT_STEPS.md). Import the first primary sources; implement standard baseline embeddings; register any empirical studies and proofs under stable IDs.

## Checks executed in this session

- `PYTHONPATH=src python -m pytest -q` — **16 passed** (includes three new research-workflow tests).
- `python scripts/validate_research.py` — **PASS** (journal link, handoff pointer, literature manifest/schema/source states, basic public API docstrings).
- `python -m compileall -q src tests scripts` — **PASS**.
- `python -m pip install -e '.[dev,docs]'` — **BLOCKED**: this sandbox cannot resolve the package index for Hatchling.
- `python -m ruff check src tests examples experiments scripts` — **NOT RUN**: Ruff not installed and package download unavailable.
- `python -m sphinx -b html -W docs docs/_build/html` — **NOT RUN**: Sphinx not installed and package download unavailable.

The CI workflow is configured to run those remaining checks on GitHub after dependency installation. The local result does not establish a successful Sphinx build.
