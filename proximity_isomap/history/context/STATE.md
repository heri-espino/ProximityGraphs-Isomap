# Current state — 2026-10-18

**Repo:** heri-espino/ProximityGraphs-Isomap. Canonical research directories: `proximity_isomap/{code,results,figures,notes}/`, matching numbered folders, immutable result run labels, historical journals in `proximity_isomap/history/`. Read AGENTS.md and AI_HANDOFF.md.

**Paper:** working research question is separation-constrained componentwise Isomap and the tradeoff between positive projected convex-hull clearance, within-manifold geodesic stress and original ambient cross-manifold placement stress. Novelty and overall superiority remain unestablished. Rigid alignment preserves only *computed* within-component pairwise distances.

**EXP-001–008:** reconstructed executable designs, versioned full run `manual-full-20261018` figures/results already in GitHub; not numerical reproductions of earlier historical code. **EXP-009:** completed exploratory VR H1 pilot, supplied K=3. **EXP-010:** cylinder versus five rings; **EXP-011:** componentwise kNN/radius Isomap and global Isomap/PCA/t-SNE/UMAP comparison; their **native executable scripts are now committed** but the new user's Windows runs are **pending**. Existing 010/011 summary plots report an older local exploratory pilot, not new user-run data. **Presentation 012** is Marp and must be updated when new results are available.

**Standing user workflow:** assistant pushes executable code; user runs locally, saves and pushes real outputs; assistant reads actual files and writes scientific Markdown and modifies Marp. Do not request ZIP downloads, use import scripts or claim results before run. The active PowerShell launcher is `scripts/run_exp_010_011.ps1`. UMAP requires `umap-learn`; no Ruff needed for experimental execution.

**Next scientific development:** after recording user outputs, study radius inference without labels, optimize separation-constrained centroid/landmark placement, test frontiers V(mu), compare D-C Isomap, M-Isomap, TopoMap and tuned UMAP/t-SNE with matched seeds/densities. See [NEXT_STEPS](NEXT_STEPS.md).
