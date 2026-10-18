# Current research state

**Updated:** 2026-10-18 (numbered experiment archive)
**Stage:** scaffold + working manuscript thesis; no validated novel result  
**Status:** exploratory; contribution not established

## 2026-10-17 — Experiment archival preparation (pending Git push)

EXP-0002–0008 have been reconciled in a local archive containing 260 experimental source/result/figure files. The importer passed 57 tests and provenance integrity checks in a simulated checkout. **These files are not yet committed to GitHub main**; see `experiments/ARCHIVE_INTEGRATION_STATUS.md`. The existing separation–distortion manuscript thesis and remote CI/Conda setup remain unchanged. Historical numerical outputs have no original source SHA and require independent reproduction after import.

## Canonical research archive (2026-10-18)

Eight coordinated experiment folders are now located under `proximity_isomap/{notes,code,figures,results}/NNN-short_title/`. EXP-001 has original GitHub-runner and smoke CSV/JSON copied by blob SHA. For EXP-002–008 only aggregate historical transcriptions and honestly labeled summary SVGs can be committed, because the full prior ZIP bundle is absent from the GitHub branch/current file workspace. These experiments **are not reproducible from this branch yet**. See `proximity_isomap/MANIFEST.json` and the latest journal for details; original `journal/` remains chronological. No new experiment was executed as part of reorganizing the record. Numbered notes/figures/results structure passed [GitHub CI](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39134370194) (tests, Ruff, two validators and Sphinx). This does not restore missing scientific assets.

## Working paper thesis (2026-10-17)

[paper/RESEARCH_DIRECTION.md](../paper/RESEARCH_DIRECTION.md) defines the agreed central research direction: independently embed graph components, align rigidly under guaranteed positive separation, and quantify the resulting tradeoff in cross-component ambient-distance fidelity. The method is a **proposal** and must be checked against prior multi-manifold Isomap, stitching and constrained alignment literature. The exact elementary geometric properties are documented in notes/results/PROP-0002-rigid-separation-frontier.md and ADR-0005 records the decision. The prior EXP-0002–EXP-0008 source/plots reside in separate local archives, not in this GitHub branch; main still only has the baseline code and EXP-0001. Do not cite those local experiment values as committed reproducible evidence. This revision changes manuscript/notes/journal only; it does not change runtime algorithms. The paper-thesis commit cc0f9dcd passed GitHub Actions run 39086961855 (pytest, Ruff, validator and Sphinx on Python 3.11/3.12); LaTeX compilation and scientific performance remain unverified.

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

## CI correction after Conda scaffolding

- First GitHub Actions run for commit `9dc79d6` installed and passed 16 tests, but Ruff reported UP017 in `experiments/run_exp_0001.py` and I001 in three scripts.
- Follow-up patch changes `datetime.now(timezone.utc)` to Python 3.11 `datetime.now(UTC)` and reduces import-block spacing. Await fresh CI to verify Ruff and Sphinx. This is a formatting-only change, not a new scientific result.

## CI verification of formatting fixes (2026-10-16)

- Commit `e7cc9bcf723e72ebec7ec0d133f03d117020b56d` passed GitHub Actions run 38997728144 on Python 3.11 and 3.12: installation, 16 tests, Ruff, `validate_research.py`, and warnings-as-errors Sphinx build.
- This validates the pip-based CI environment only, **not** the root Conda environment solve. No new embedding algorithm or research comparison was validated by this run.
