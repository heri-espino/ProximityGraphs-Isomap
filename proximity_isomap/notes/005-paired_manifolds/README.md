# EXP-005 — Two disconnected Swiss rolls and two disconnected S-curves

**Research question.** What happens when dimensionality reduction must embed **two genuine manifolds in one 3D dataset**, rather than a single curved sheet?

## Design

Two data families: pairs of Swiss rolls and pairs of S-curves, with 45 observations on each surface (90 per dataset). Their original x-coordinate ranges were moved apart to guarantee an interval with **exactly two graph components**, each internally connected. A 44-candidate radius grid included graph-topology transitions; α=0.5, one nonlinear optimizer start. PCA, radius hybrid MDS and kNN Isomap were compared; 3D originals and 2D projection galleries were saved in the historical ZIP archive.

## Selected historical single-seed results

| Geometry and method | Within-sheet intrinsic stress | Between-sheet ambient stress |
|---|---:|---:|
| Swiss PCA | 0.7355 | 0.0106 |
| Swiss hybrid, two components | 0.7026 | 0.0799 |
| Swiss hybrid, newly connected | 0.7173 | 0.2603 |
| S-curve PCA | 0.4192 | 0.0562 |
| S-curve hybrid, two components | 0.3696 | 0.1856 |
| S-curve hybrid, newly connected | 0.3197 | 0.7299 |

## Interpretation

**Disconnected underlying manifolds do not have finite intrinsic geodesics between them.** Thus the within-sheet stress uses known intrinsic distances, whereas the between-sheet metric uses original **ambient** Euclidean distances. On the S-curve example, the first bridge improved the within-sheet stress while heavily worsening between-sheet placement. We must never collapse the two metrics into an undefined “global intrinsic stress.”

## Open questions

The original PNG/SVG gallery cannot be reconstructed exactly from rounded scores. It awaits a fresh run of the reconstructed protocol (we will not import the historical ZIP). One seed and untuned baselines preclude population claims. EXP-006 introduces a harder orientation intervention to stress global PCA.



## Mathematics: two different distance targets

For two generating sheets \(C_1,C_2\), *within* stress uses the known analytic intrinsic distances \(d_{ij}^{\mathrm{true}}\) of each sheet, whereas *between* stress uses original **ambient** distances \(a_{ij}=\|x_i-x_j\|_2\):

$$
E_{\mathrm{within}}(Y)=
\sqrt{\frac{
\sum_{k=1}^{2}\sum_{i<j,\ i,j\in C_k}
(\|y_i-y_j\|_2-d_{ij}^{\mathrm{true}})^2
}{
\sum_{k=1}^{2}\sum_{i<j,\ i,j\in C_k}
(d_{ij}^{\mathrm{true}})^2
}},
$$

$$
E_{\mathrm{between}}(Y)=
\sqrt{\frac{
\sum_{i\in C_1,\ j\in C_2}
(\|y_i-y_j\|_2-\|x_i-x_j\|_2)^2
}{
\sum_{i\in C_1,\ j\in C_2}\|x_i-x_j\|_2^2
}}.
$$

Both denominators must be positive. In the disconnected *intrinsic* manifold space, a path between \(C_1\) and \(C_2\) does not exist; a cross-component ambient distance is **not** a geodesic.

**Interpretation:** adding a graph bridge can improve one error while worsening the other. Plot the two stresses separately and never interpret a reduced ambient cross-stress as proof of better intramanifold geometry.

## Figure plan and reproduction status

**Full rebuilt run pending:** the runner will save PNG and SVG files and embed valid PNG links after a successful full run; do not create links to absent files. Existing historical `summary.svg` above is already visible and clearly identified as a reconstruction.

| Planned output filename | Mathematical point to illustrate | Current status |
|---|---|---|
| `swiss_pair.png` | Two Swiss rolls: 3D original and 2D method comparison | Pending full rerun |
| `s_curve_pair.png` | Two S-curves: geodesic-vs-ambient tradeoff | Pending full rerun |

**After a new run:** confirm that image filenames and actual metric fields match the notes before interpreting the figures. [Plot directory](../../figures/005-paired_manifolds/README.md) · [Result directory](../../results/005-paired_manifolds/README.md).

## Linked artifacts

- [Code and source status](../../code/005-paired_manifolds/README.md)
- [Numerical results and provenance](../../results/005-paired_manifolds/README.md)
- [Summary diagram](../../figures/005-paired_manifolds/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/005-paired_manifolds/README.md)

**Research status:** Historical figures/numbers are transcriptions, not outputs of the new reconstructed source. A fresh full run is pending; no integration ZIP will be imported.

## Historical summary figure (not a new run)

![Historical experiment 005-paired_manifolds summary — source-transcribed diagnostic values](../../figures/005-paired_manifolds/summary.svg)

> This SVG is a reconstructed visualization of historical rounded summaries, not a recovered 3D/2D projection. Actual figures will be embedded automatically under the latest computed run after executing the Conda pipeline.
