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



## Mathematics: the hybrid target and embedding stress

For a finite graph component, let \(g_{ij}(r)\) be the graph-shortest-path distance and \(a_{ij}=\|x_i-x_j\|_2\) the original ambient distance. A reconstructed hybrid dissimilarity is

$$
D_{ij}^{(\alpha,r)}=
\begin{cases}
\alpha g_{ij}(r)+(1-\alpha)a_{ij}, &
i,j\text{ in the same graph component},\\
a_{ij},&i,j\text{ in different components}.
\end{cases}
$$

A possible 2D metric-MDS target is

$$
\min_{Y\in\mathbb R^{n\times 2}}
\sum_{i<j}\left(\|y_i-y_j\|_2-D_{ij}^{(\alpha,r)}\right)^2.
$$

This defines the **current reconstructed SMACOF baseline**, which is not identical to the older *weighted-stress* optimizer. A hybrid matrix need not be a true metric (it may violate the triangle inequality), so a zero-distortion Euclidean embedding need not exist.

**Interpretation:** the objective can prioritize cross-component ambient placements over true intrinsic unfolding. Assess its training loss and its separately computed true-intrinsic stress; do not call them the same measurement.

## Figure plan and reproduction status

**Full rebuilt run pending:** the runner will save PNG and SVG files and embed valid PNG links after a successful full run; do not create links to absent files. Existing historical `summary.svg` above is already visible and clearly identified as a reconstruction.

| Planned output filename | Mathematical point to illustrate | Current status |
|---|---|---|
| `single.png` | Single Swiss roll: original 3D, PCA, hybrid and separated component embeddings | Pending full rerun |
| `pair.png` | Two Swiss rolls: cross-component overlap and local geometry | Pending full rerun |

**After a new run:** confirm that image filenames and actual metric fields match the notes before interpreting the figures. [Plot directory](../../figures/002-hybrid_mds/README.md) · [Result directory](../../results/002-hybrid_mds/README.md).

## Linked artifacts

- [Code and source status](../../code/002-hybrid_mds/README.md)
- [Numerical results and provenance](../../results/002-hybrid_mds/README.md)
- [Summary diagram](../../figures/002-hybrid_mds/summary.svg) — conceptual flow diagram
- [Figure directory and original-plot status](../../figures/002-hybrid_mds/README.md)

**Research status:** Historical figures/numbers are transcriptions, not outputs of the new reconstructed source. A fresh full run is pending; no integration ZIP will be imported.

## Historical summary figure (not a new run)

![Historical experiment 002-hybrid_mds summary — source-transcribed diagnostic values](../../figures/002-hybrid_mds/summary.svg)

> This SVG is a reconstructed visualization of historical rounded summaries, not a recovered 3D/2D projection. Actual figures will be embedded automatically under the latest computed run after executing the Conda pipeline.

<!-- COMPUTED-RUN: manual-full-20261018 -->

## Computed run: manual-full-20261018

Run: **manual-full-20261018**; mode: **full**; seed: **20261018**. This run REBUILDS the research question using the current implementation; it is **not the recovered historical algorithm or an independent novelty claim**. Original arrays and metrics: [results](../../results/002-hybrid_mds/runs/manual-full-20261018/metrics.csv); [metadata](../../results/002-hybrid_mds/runs/manual-full-20261018/metadata.json).

| K | Method | Within intrinsic stress / diagnostic RMSE | Between ambient stress |
|---:|---|---:|---:|
| 1 | PCA | 0.7522263174507533 | None |
| 1 | Hybrid_MDS | 0.5973505652263034 | None |
| 1 | Component_Isomap_free | 0.5508490989671648 | None |
| 1 | Component_Isomap_separated | 0.5508490989671648 | None |
| 2 | PCA | 0.7571423575319229 | 0.034956686234189085 |
| 2 | Hybrid_MDS | 0.6295947372371044 | 0.1265500325200276 |
| 2 | Component_Isomap_free | 0.511078098804458 | 0.33272022966545217 |
| 2 | Component_Isomap_separated | 0.511078098804458 | 0.7621924913618394 |

![New 002 plot: pair](../../figures/002-hybrid_mds/runs/manual-full-20261018/pair.png)
![New 002 plot: single](../../figures/002-hybrid_mds/runs/manual-full-20261018/single.png)
