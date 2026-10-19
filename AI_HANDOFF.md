# AI handoff — ProximityGraphs-Isomap

**Updated 2026-10-19.** Read [AGENTS.md](AGENTS.md), the [experiment notes](proximity_isomap/notes/README.md), the [latest dated journal](proximity_isomap/history/journal/LATEST.md), the [2026-10-19 research entry](proximity_isomap/history/journal/2026-10/2026-10-19-componentwise-knn-marp-lecture.md), and [current research state](proximity_isomap/history/context/STATE.md) before new work.

## Mandatory three-stage experiment workflow

**Assistant commits code and mathematical pre-run figure plan** under proximity_isomap; **user runs locally on Windows and pushes actual CSV/NPZ/JSON and PNG/SVG evidence**; **assistant reads the exact pushed results, writes mathematical Markdown with real embedded figures, and updates the Marp presentations**. No ZIP-only handoff, invented results or heavy automatic push-triggered computation. A prepared EXP-013 is not the same as an executed EXP-013.

## Verified research and presentation status

- Reconstructed EXP-001–008 have versioned full-run figures, distinct from historical rounded summaries. EXP-009 has a published VR H1 exploratory pilot with supplied K=3.
- **EXP-010** cylinder versus five genuinely separate circles: actual Windows run 20261019T061001Z-full is in GitHub; [scientific note](proximity_isomap/notes/010-radius_density_and_rings/README.md) now includes measured CSV values and all four original PNG figures. This is fixed-scale VR H1, not a full persistent barcode.
- **EXP-011** componentwise radius/kNN Isomap against global Isomap, PCA, t-SNE and **genuine executed UMAP**: actual Windows run 20261019T061001Z-full is in GitHub; [scientific note](proximity_isomap/notes/011-isomap_baselines/README.md) includes measured CSV comparisons, negative findings and all eight actual PNG panels.
- The current EXP-011 method does **not** detect components with a global kNN graph. Its detector uses radius or *supplied-K* MST cut; it rebuilds **symmetrized 10-NN within each detected component**. Its placement is a simple rigid strip heuristic, not globally optimized centroid/landmark alignment.
- **Checkpoint 012** includes the expanded [main Marp presentation](proximity_isomap/notes/012-presentation_checkpoint/presentation.md) and a standalone [53-slide mathematical lecture](proximity_isomap/notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md) on componentwise kNN-Isomap. Both embed actual GitHub run figures; lecture deliberately distinguishes proven statements, measured results and proposed EXP-013.
- EXP-013 is **proposed only**: systematically sweep distinct kNN detection and embedding parameters, and later compare constrained centroid/landmark placement. Code and experiments not claimed complete.

## Mathematical and paper boundaries

Internal computed distances survive orthogonal motions exactly; intrinsic geodesic distances need not be recovered exactly by Isomap. Cross-component intrinsic geodesics are infinite/undefined on disconnected supports; the placement objective uses finite original **ambient** distances. Centroid-only alignment does not determine orientations if local embeddings are centered. A feasible strip layout guarantees geometric clearance but can have poor intercomponent ambient-distance stress. Rigid invariance, graph component nesting and the monotonic frontier are elementary, not novelty claims. Confront D-C Isomap, M-Isomap, S-Isomap++, TopoMap, DIPOLE and other prior work.

## What to do next

Render and inspect the new Marp deck locally (instructions in 012 README). For specialized EXP-013, first **commit code/tests/pre-run note**; have the user run and push unique full-run files; only then interpret experiment results and update the lecture. Preserve earlier run records, failed methods and provenance.


## EXP-013 code checkpoint — 2026-10-19

The user requested a deliberately large, shared-research Marp notebook with all mathematical lessons, successful/failed near/far cases and every 3x3 dashboard. An EXP-013 runner has been committed at `proximity_isomap/code/013-classical_multicomponent_dashboards/run.py`, Windows launcher `scripts/run_exp_013.ps1`, tests `tests/test_exp013_classical_dashboards.py`, and full pre-run math/figures plan under `proximity_isomap/notes/013-classical_multicomponent_dashboards/README.md`. It includes 7 geometry families × far/near = 14 scenarios, two dashboards of 9 methods each per scenario (12 unique methods), and a k_detect/k_embed grid. **The user has not yet run EXP-013; no generated results or figures are claimed.** Next: user executes quick pytest/smoke/full and pushes; assistant reads actual files and adds all 28 generated dashboards and evidence-grounded interpretation to note 013 and Marp checkpoint 012. Never drop failures or oracle-K caveats.
