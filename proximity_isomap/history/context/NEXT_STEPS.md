# Next steps — 2026-10-18

## EXP-010 and EXP-011: current checkpoint

- [x] Commit Python executables under `proximity_isomap/code/010-radius_density_and_rings/` and `011-isomap_baselines/`.
- [x] Commit `scripts/run_exp_010_011.ps1`, lightweight unit tests, math notes and figure plans.
- [x] Record in AGENTS.md: assistant authors code → user runs/pushes data → assistant interprets actual evidence and updates notes.
- [ ] User: `git pull --ff-only`; install `umap-learn` in `proximity-isomap` environment.
- [ ] User: run `.\scripts\run_exp_010_011.ps1 -Quick` for smoke (ignored by Git).
- [ ] User: run `.\scripts\run_exp_010_011.ps1 -RequireUmap` for the full experiment.
- [ ] User: inspect generated metrics/figures; commit/push only original **full** `proximity_isomap/results/010*,011*` and `figures/010*,011*` run folders.
- [ ] Assistant: retrieve latest actual run, verify metadata and saved arrays; interpret numerical/visual findings and update 010/011 scientific Markdown with *actual* inline PNGs.
- [ ] Assistant: update [Marp presentation 012](../../notes/012-presentation_checkpoint/README.md), handoff and dated journal after the scientific analysis.

## Later scientific work

- [ ] Infer radius and number of components without known labels/K; measure failures and probabilistic radius-recovery window under variable sampling/noise.
- [ ] Compare source-verified D-C Isomap, M-Isomap, S-Isomap++ and TopoMap variants rather than merely relabeling componentwise Isomap.
- [ ] Optimize relative rigid centroid/landmark placement with strict convex-hull clearance, characterize separation–ambient-distortion frontier.
- [ ] Run multiple independent seeds, diverse manifold families and carefully tuned standard/global PCA/Isomap/t-SNE/UMAP comparisons.
- [ ] Review the Marp PDF rendering before presenting to the professor.

**GitHub publication rule:** an experiment is complete only when its executed source, exact metric/array outputs, real figures, and explanatory notes are verified on GitHub. An unrun source is `prepared`, not `completed`.
