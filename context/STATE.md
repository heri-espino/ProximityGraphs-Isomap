# Current research state

**Updated:** 2026-10-16  
**Stage:** repository scaffold, no validated results  
**Status:** exploratory; contribution not established

## Goal

Study proximity graphs, especially disconnected radius graphs, as a substrate for geodesic approximation and dimensionality reduction. Compare standard Isomap, Euclidean MDS/PCA, hybrid weighted stress, and componentwise embedding/alignment fairly.

## Established definitions

- Graph rule `||x_i-x_j||_2 <= r` and edge weight `||x_i-x_j||_2`; see `notes/definitions.md`.
- Intracomponent graph distances and intercomponent ambient distances can be combined into a finite **dissimilarity**, not necessarily a metric.
- Distortion objectives should be reported separately for within- and between-component pairs.

## Implemented and tested

- Radius-graph builder with Euclidean edge weights and component labels.
- Hybrid dissimilarity matrix (graph shortest-path inside; ambient Euclidean outside).
- Normalized weighted within/between stress **evaluation** (not yet an embedding optimizer).
- Minimal reproducible synthetic Swiss-roll radius-sweep experiment with analytic intrinsic distances.

## Not yet implemented or proven

- Optimizers for hybrid stress or rigid component alignment.
- A graph-region abstraction for Gabriel, RNG, beta-skeleton or general unit-region templates.
- Benchmark comparisons against tuned Isomap and metric MDS.
- Any novel theorem, statistical rate, or empirical result.

## Repository and literature workflow

- `AGENTS.md` requires reading the latest dated research journal before summarized state. `AI_HANDOFF.md` captures current operational context and must be updated when substantive files change.
- `literature/pdf/`, `literature/markdown/`, and `literature/references/` distinguish originals, unverified Docling extraction, and verified source annotations. `literature/MANIFEST.csv` and `references/KEY_RESULTS.md` track review status and theorem provenance. **No paper PDFs or reviewed results are included yet.**
- `scripts/new_literature_entry.py` registers an unreviewed paper; `scripts/validate_research.py` checks record consistency and public API docstrings. `scripts/check_change_protocol.py` requires a new journal and updated handoff/state files in research-changing pull requests.
- Local verification: 16 tests passed, structural validator passed, Python compileall passed. Ruff/Sphinx not run because these packages were unavailable offline; CI config includes both.
- Manuscript citations use the canonical `literature/references/library.bib`.

## Important caution

Using Euclidean distances to arrange disconnected components can preserve ambient fold proximity rather than intrinsic separation. Experiments must measure true intrinsic distances on synthetic manifolds where available.

## Source-of-truth pointers

- Next priorities: `context/NEXT_STEPS.md`.
- Decisions: `context/DECISION_INDEX.md`.
- Definitions: `notes/definitions.md`.
- First protocol: `experiments/EXP-0001.md`.

## Conda and first EXP-0001 smoke run (2026-10-16)

- Added `environment.yml` (Conda Python 3.11, conda-forge scientific, documentation and benchmark tools, editable project install).
- Locally ran 16 tests (passed) and the EXP-0001 script from an extracted starter ZIP using plain Python, **not Conda** and **not a Git checkout**. At radii [1.5, 2.5, 3.5, 5, 7], measured intracomponent geodesic RMSE [1.05246, 2.13986, 3.02933, 1.23956, 26.27899] on 240 synthetic points. The measured pair sets vary with radius, so this is exploratory only. Git SHA not recorded.
- Must still solve/test the Conda environment, run Ruff/Sphinx, and rerun from the checked-out revision before considering a documented research result.
