# Legacy figures directory

Canonical experiment-specific graphics are now indexed under [proximity_isomap/figures/](../proximity_isomap/figures/README.md). Newly drawn summary SVG charts are present for all eight experiments; the original historical 3D and 2D projection PNG/SVG figures for 002–008 remain missing until the research ZIP is imported. The existing paper figure directory is retained.


- `scripts/`: version-controlled plotting source (create as needed).
- `paper/`: **publication-ready** PDF/SVG/PNG figures referenced by LaTeX (commit selected outputs so a fresh checkout can compile the paper).
- `exploratory/`: temporary plots, not for publication (Git-ignored).

Figure scripts should read `results/` summaries or regenerate datasets deterministically. No screenshots of experimental outputs without reproducible plotting scripts.
