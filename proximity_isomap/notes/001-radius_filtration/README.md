# EXP-001 — Radius graph filtration on one Swiss roll

**Research question.** Can an undirected radius-proximity graph recover the geodesic geometry of a sampled Swiss roll, and how does the radius change connectivity?

## Idea and setup

A ball of radius r centered on each observation induces edges when **center distance ≤ r** (not when two r-balls intersect at 2r). The graph is weighted by the ambient Euclidean distance between endpoints. The 240-point noiseless Swiss roll has intrinsic coordinates `(u(t),h)`, with `u(t)=[t√(1+t²)+asinh(t)]/2`. The original smoke test used radii 1.5, 2.5, 3.5, 5, 7 with seed 20261016.

## What we did

Constructed each graph, measured its connected components and edges, computed shortest paths and compared **only finite, within-graph-component pairs** against analytical intrinsic distances. No embedding coordinates were optimized in EXP-001.

## Recorded outcome

| Radius | Components | Edges | Within pairs | Graph versus intrinsic RMSE |
|---:|---:|---:|---:|---:|
| 1.5 | 88 | 231 | 776 | 1.0525 |
| 2.5 | 16 | 618 | 5,832 | 2.1399 |
| 3.5 | 3 | 1,169 | 23,473 | 3.0293 |
| 5 | 1 | 2,189 | 28,680 | 1.2396 |
| 7 | 1 | 4,431 | 28,680 | 26.2790 |

## Interpretation and failure

Connectivity improves with radius, but the shortest paths can become **shortcuts through folds** at large radius. The extreme error at r=7 is the key diagnostic. **Do not compare the small-radius RMSE directly with the large-radius RMSE as if they evaluate identical pairs**: the finite-pair set changes when components merge.

## Next question

Evaluate all original pairs against the same intrinsic reference by constructing complete 2D embeddings (EXP-002), then vary r across much wider regimes (EXP-003). A usable radius must be selected without looking at test-set ground truth.


## Linked artifacts

- [Code and source status](../../code/001-radius_filtration/README.md)
- [Numerical results and provenance](../../results/001-radius_filtration/README.md)
- [Summary diagram](../../figures/001-radius_filtration/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/001-radius_filtration/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.

## Historical summary figure (not a new run)

![Historical experiment 001-radius_filtration summary — source-transcribed diagnostic values](../../figures/001-radius_filtration/summary.svg)

> This SVG is a reconstructed visualization of historical rounded summaries, not a recovered 3D/2D projection. Actual figures will be embedded automatically under the latest computed run after executing the Conda pipeline.

