# EXP-002 — Comparing PCA, Isomap and hybrid dissimilarity MDS

**Research question.** If the radius graph is disconnected, can we preserve graph geodesics *within* components and ambient Euclidean distances *between* components in a single 2D projection?

## Idea

Define a hybrid distance target: weighted shortest-path length for observations connected in the radius graph, and original Euclidean distance for pairs in different graph components. Fit 2D coordinates with normalized pairwise stress; compare PCA, conventional connected Isomap, radius Isomap, and hybrid weighted MDS using the **same observations**.

## What we tried

A small exploratory Swiss-roll benchmark, alongside optimizing a mixing weight α between within- and between-component distances. Multiple initializations and fair edge-density or hyperparameter matching were not yet established. The hybrid target need not satisfy the triangle inequality.

## Observations

The early comparison exposed a failure: Euclidean distances across folded or disconnected regions can conflict with intrinsically correct geodesic distances, pulling the projected configuration into a distorted compromise. This motivated evaluating **intrinsic stress independently of the fitting target**. Its initial smoke plots and exact numerical CSVs are missing from GitHub main, so no numerical score is asserted here.

## Interpretation

We should not describe a lower hybrid *training stress* as an improvement to true manifold recovery. Disconnected shortest paths also make standard Isomap's global distance matrix undefined unless a clear policy is specified. This benchmark motivated controlling the radius and separating component alignment from intracomponent optimization.

## Next question

Repeat over the complete scale range—including no-edge and complete graphs—with exact graph-transition diagnostics (EXP-003).


## Linked artifacts

- [Code and source status](../../code/002-hybrid_mds/README.md)
- [Numerical results and provenance](../../results/002-hybrid_mds/README.md)
- [Summary diagram](../../figures/002-hybrid_mds/summary.svg) — conceptual flow diagram
- [Figure directory and original-plot status](../../figures/002-hybrid_mds/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.
