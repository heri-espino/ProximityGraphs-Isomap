# Legacy results index

The canonical experiment-facing results and provenance directories are at [proximity_isomap/results/](../proximity_isomap/results/README.md). The old `results/exp_0001/smoke/` data and `EXPLORATORY_OVERVIEW.md` are retained for historical provenance, and the EXP-001 original is copied into the numbered archive.

No historical EXP-002–008 raw experimental arrays are present on this branch. Reproducing old charts from rounded summary tables is **not** the same as recovering the original runs.


Small scientific outputs (`metrics.csv`, `metadata.json`, compact tables) may be committed once checked. Large prediction matrices, intermediate arrays and cache directories are ignored. Never overwrite a published run ID; use a new output folder for reruns.

Every manuscript figure or table must cite an experiment ID and, when possible, a commit SHA. The source configuration belongs under `experiments/configs/`.
