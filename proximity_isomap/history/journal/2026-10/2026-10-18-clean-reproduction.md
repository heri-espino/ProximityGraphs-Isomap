# 2026-10-18 — Remove legacy root folders and rebuild all eight experiments

## Decision
The user requested a clean canonical `proximity_isomap/` area, inline Markdown figures, rebuilt experimental code rather than importing Integration.zip, a pinned ContrastColors dependency, and a single Conda PowerShell pipeline.

## Changes
- Moved journal, decisions, context, legacy experiment protocols, old raw smoke tables and mathematical notes into `proximity_isomap/history/` or `proximity_isomap/notes/mathematics/`, preserving old content as evidence.
- Removed obsolete root folders after copying Git blobs; retained reusable Python code in `src/proximity_isomap/` and Sphinx/manuscript/literature folders.
- Added `proximity_isomap/code/research_runner.py` and 002..008 wrappers: these are **new reconstructions of the historical questions**, not bit-exact original solvers. Implemented radius diagnostics, global hybrid dissimilarity MDS, PCA, componentwise Isomap, a rigid alignment heuristic with guaranteed ordered x-gap, density transfer and the 1–6 roll case.
- Pinned user-owned ContrastColors version `84e05b40b6ba6aa6864f5bc13ad43da3c4c1e93d` in Conda environment for white scientific plots. Added `scripts/run_all.ps1` for environment creation, tests, repeated runs, figures, notes, and optional explicit Git push.
- Existing historical SVG summary plots are embedded inside 001..008 Markdown notes and labeled historical. Upon actual local execution, a new run adds actual PNG/SVG panels to a single current-result section in the same note.

## Evidence/limits
No full 001–008 experiment was executed by this commit on the user's machine. The runner is new code, and its output may differ from the old historical rounded tables. The synthetic component radius is label-informed and EXP-004 development tuning uses analytic truth. One-start and rigid-alignment heuristics are exploratory, not a globally optimal frontier or proof of novel performance.

## Verification and next action
Source is submitted to GitHub CI; record checks after completion rather than claiming them in advance. The user should run `./scripts/run_all.ps1 -Quick` and then `./scripts/run_all.ps1 -Push` in their own Conda-enabled PowerShell, inspect figures and record new Git SHA. Do not import Integration.zip.
