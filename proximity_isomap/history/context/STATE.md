# Current state — 2026-10-19

**Research project:** ProximityGraphs-Isomap. Canonical numbering: EXP-010 cylinder/rings, EXP-011 Isomap baseline comparison, checkpoint 012 Marp presentation, EXP-013 proposed specialized study.

## Completed evidence

- EXP-001–008 rebuilt experiments and EXP-009 topology pilot have GitHub-published numerical/visual evidence, distinct from historical rounded summaries.
- **EXP-010** full Windows run 20261019T061001Z-full is committed under corresponding results and figures folders; the numbered note embeds four real PNGs and explains fixed-radius component/VR-homology measurements.
- **EXP-011** full Windows run 20261019T061001Z-full is committed; UMAP actually ran. The note embeds eight real PNGs and compares within-geodesic stress, trustworthiness, centroid distortion and projected convex-hull overlap. One seed, supplied K in some diagnostics, and disconnected graph reconnection for standard Isomap remain limitations.
- Checkpoint 012 main Marp has been expanded with the computed EXP-010/011 plots and mathematical derivations, plus a 53-slide standalone componentwise kNN-Isomap lecture. PDF/PPTX visual rendering has not been verified.

## Permanent workflow

The assistant commits experiment code and pre-run math; the user runs the heavy experiments locally and pushes numerical/visual outputs; the assistant analyzes those specific files and writes post-run Markdown interpretation and updates the slides. Do not send ZIPs as substitutes or present proposed runs as completed. This is documented in AGENTS.md.

## Research directions

The present EXP-011 "componentwise kNN" method uses radius/supplied-K MST component discovery and *within-component* 10-NN, not global unsupervised kNN discovery. Proposed EXP-013 should distinguish k_detect and k_embed; characterize connectivity and partition errors, intracomponent graph-geodesic reconstruction and convex-hull clearance/cross-placement tradeoffs across k and sampling regimes. Optimization of the separation–distortion frontier remains proposed, not validated novelty.
