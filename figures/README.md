# Figures

- `scripts/`: version-controlled plotting source (create as needed).
- `paper/`: **publication-ready** PDF/SVG/PNG figures referenced by LaTeX (commit selected outputs so a fresh checkout can compile the paper).
- `exploratory/`: temporary plots, not for publication (Git-ignored).

Figure scripts should read `results/` summaries or regenerate datasets deterministically. No screenshots of experimental outputs without reproducible plotting scripts.
