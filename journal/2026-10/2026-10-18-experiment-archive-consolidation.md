# 2026-10-18 — Consolidate the eight experiments into numbered research notes

**Status:** Repository organization and evidence indexing; no new manifold-learning experiment executed in this migration.

## Request and design

The user wants the experiment's motivation, attempts, findings, failures and interpretations in a single note, cross-linked to corresponding code, results and figures under `proximity_isomap/`. Canonical numbered slug folders now match across `notes/`, `code/`, `figures/` and `results/` for EXP-001 through EXP-008.

A deliberate naming decision preserves the true experiment chronology: **007-component_alignment** is the two-roll alignment experiment; **008-multiple_swiss_rolls** is the K=1..6 extension. The example “007-multiple_swiss_rolls” in the request was illustrative, not a request to renumber historical experiment IDs.

## Evidence audited

- GitHub main contained runnable source, frozen config and original smoke CSV/JSON **only for EXP-001**.
- `experiments/ARCHIVE_INTEGRATION_STATUS.md` documented a previously prepared *260-file* historical integration bundle for EXP-002..EXP-008, but its source, NPZ/CSV files and PNG/SVG projections were still not on GitHub. This session did not have that ZIP in its current working environment.
- The repository's `results/EXPLORATORY_OVERVIEW.md` and chronological chat contained **rounded numerical summaries**, which were transcribed into clearly labeled `summary.csv` files and explanatory notes. Those numerical summaries have not been recomputed on main.

## Changes

- Added `proximity_isomap/{notes,code,figures,results}/` with stable folders for IDs 001–008, navigation and machine-readable availability manifest.
- Migrated exact original EXP-001 script, config, smoke metrics and metadata by Git blob reference, without modifying data.
- Added eight detailed experiment notes with question, design, results, negative findings, interpretation and links to corresponding actual SVG summary diagrams.
- Created vector SVG summary diagrams from rounded reported aggregate tables and a conceptual diagram for 002; **these are not the original saved 3D data or projection figures**.
- Created code/reproducibility ledgers for each missing original script/data/figure. Added `scripts/restore_experiment_archive.py` as a no-overwrite, dry-run-default helper for moving files from the previously produced archive.
- Added structural validator `scripts/validate_experiment_archive.py` and tests, and updated the README, AI handoff, context and research workflow.

## Why this separation of responsibilities

The edited `proximity_isomap/notes/NNN-...` note is the canonical per-experiment scientific record. `journal/` remains chronological and append-only for research decisions and failures; `paper/` is concise scientific synthesis. Duplicating the entire journal in experiment notes would make facts drift.

Reusable Python package code remains in `src/proximity_isomap/` and is **not** moved into the research document folder, so the editable install and Sphinx library API remain intact. Root `experiments/`, `figures/`, and `results/` retain historic compatibility references until the 260-file original bundle is mapped and validated.

## Limits, verification and next task

This restructuring does **not** recover missing historical source or authentic 3D/2D PNG figures. Do not claim the eight experiment records are all rerunnable; their explicit provenance ledgers document exactly what is missing. No true cross-component intrinsic geodesics are fabricated.

GitHub CI is configured to run the new archive validator and tests, including archive directory/link checks; results must be inspected **after committing**. No local scientific computation or hash verification of the old 260-file ZIP occurred in this task.

Next: obtain the original research integration ZIP, verify SHA-256 manifests, dry-run the restoration helper, then import missing sources/plots/arrays and reproduce under a Git commit SHA. Only then should notes mark those original artifacts complete.
