# EXP-003 — Radius sweep from isolated observations to a complete graph

**Research question.** Does the best geometric fidelity occur near graph connectivity, and what happens when the radius is extremely small or extremely large?

## Experimental design

Use a dimensionless radius `ρ=r/ℓ` where `ℓ` is the observed median tenth-nearest-neighbor distance. Explore logarithmic candidates from 0.001ℓ to 100ℓ, plus anchors around the Euclidean MST connectivity threshold and complete-graph threshold. Fix hybrid α=0.5. Cache unchanged graphs because radius edge sets are nested.

## Observed behavior

The 85-point noiseless Swiss-roll **single-seed smoke** scan contained 42 candidate radii but only 19 distinct graphs. Hybrid intrinsic stress was about 0.7075 at both extremes; its lowest *within-dataset oracle* observed stress was about 0.0969 at ρ≈0.919, with a connected graph. There was an abrupt degradation near ρ=1.0 despite no new component merge.

A separate three-seed, 120-point exploratory scan used 82 radii per seed and found best within-dataset stresses 0.0678, 0.0698 and 0.0509 at ratios near the MST connectivity threshold.

## Interpretation

A wide grid matters: tiny radii give few/no intracomponent edges and large radii create Euclidean shortcuts or complete-graph behavior. The optimum can be sharp. The minima quoted above were chosen using true geodesic distances **on the same sample**, so they are oracle diagnostics rather than deployable unsupervised radius selection.

## Failure and next question

A larger five-seed run was interrupted before writing aggregate outputs. EXP-004 therefore tests radius transfer with separate development and evaluation datasets, and later runners should checkpoint per sample.


## Linked artifacts

- [Code and source status](../../code/003-wide_radius_grid/README.md)
- [Numerical results and provenance](../../results/003-wide_radius_grid/README.md)
- [Summary diagram](../../figures/003-wide_radius_grid/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/003-wide_radius_grid/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.
