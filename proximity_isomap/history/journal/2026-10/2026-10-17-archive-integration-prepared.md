# 2026-10-17 — Prepared complete experimental history for Git integration

**Status:** Full local integration package verified, **not yet uploaded into GitHub main**. This entry records the pending import transparently.

## Context and archive inventory

Previous sessions produced EXP-0002 through EXP-0008 as separate ZIP archives, instead of committing the scientific source and output together. The EXP-0008 archive was cumulative except for one EXP-0002 embedding NPZ recovered from its original ZIP. A conflict-aware integration archive was built from all seven snapshots and retains 260 archived files: new Python optimizers, experiment scripts/configs, tests, per-run CSV/JSON/NPZ outputs (including checkpoints), 3D/2D PNG/SVG graphics and plotting scripts, seven original dated research entries, mathematical notes and the previous failure records.

The package has an SHA-256 manifest and a one-command local importer. It merges *additively* into a current clone of this repository; it never overwrites the newer paper thesis, Conda environment, or CI. The local six-component separation proof was renamed PROP-0003 so it cannot collide with the present paper's PROP-0002.

## Local verification

- Extracted EXP-0008 scientific source: **57 pytest tests passed**; research validator passed.
- Imported into a clean simulated checkout: **57 tests passed**, validator passed, all 260 SHA-256 file hashes verified, and the existing manuscript was preserved.
- Python compilation passed. No confirmed local Ruff or Sphinx run. Previous successful GitHub CI tested only the earlier scaffold and paper outline.
- The imported historical numerical outputs do **not** come from a versioned Git checkout: integration does not retroactively prove numerical reproducibility or novelty.
- The binary archive remains available in the originating ChatGPT conversation as `ProximityGraphs-Isomap-Research-History-Integration.zip`. This is **not** a GitHub-hosted download URL.

## Scientific progression and caveats

EXP-0002–3 investigated geodesic distortion across a wide radius grid, observing abrupt shortcut/connectivity transitions. EXP-0004 tested density shift and showed a fixed development-selected radius can transfer poorly. EXP-0005 separated intrinsic within-manifold fidelity from ambient cross-manifold placement. EXP-0006 rotated two Swiss rolls, exposing global PCA's limits and the hybrid method's placement tradeoff. EXP-0007 introduced rigid componentwise alignment with guaranteed non-overlap. EXP-0008 generalized strict separation to one through six Swiss rolls, but used label-informed diagnostic radii and a single primary sample per component count. These remain exploratory claims, not a fair final benchmark or proof of novelty.

## Immediate action

From a *clean current Git clone* extract the generated integration ZIP and run `python research-import/import_into_repo.py ./ProximityGraphs-Isomap --commit`. Run CI and its provenance checker, then `git push origin main`. The importer will add a newer dated journal entry, update the index/handoff and stage historical figure/data files normally ignored by Git. Do **not** announce integration as complete until that push is confirmed. Afterwards rerun representative experiments under the resulting commit SHA and a pinned environment.
