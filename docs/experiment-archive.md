# Recomputed numbered experiments

Every experiment has linked notes, code, figures and results in [the canonical research archive](https://github.com/heri-espino/ProximityGraphs-Isomap/tree/main/proximity_isomap).

Execute from a Windows PowerShell session using `./scripts/run_all.ps1 -Quick` (smoke) or `./scripts/run_all.ps1 -Push` (full recomputation plus Git push).

The environment pins the author's [ContrastColors](https://github.com/heri-espino/Colors) plotting library. Newly computed PNG and SVG figures are recorded beside reproducible metric CSV, metadata JSON and coordinate NPZ data, then linked and **embedded** into each experiment's Markdown note.

Old root journaling/context is preserved under `proximity_isomap/history/` rather than scattered across top-level folders. The 002–008 experiments are newly reconstructed and are not exact old-source recovery.
