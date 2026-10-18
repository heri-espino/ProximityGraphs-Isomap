# EXP-008 — From one to six separately embedded Swiss rolls

**Research question.** Can rigid componentwise Isomap scale from **1 through 6** genuinely disjoint rotated Swiss rolls while guaranteeing geometric non-overlap in 2D?

## Design

For each K=1,…,6, sample **180 points per roll** (180–1080 observations), seed 20261017, with different 3D orientations and original x-bounding-box gaps. Select the graph radius slightly larger than the **maximum within-true-roll Euclidean MST edge**. This uses known synthetic labels and is therefore a diagnostic radius, not an unsupervised model-selection procedure. Fit global PCA, hybrid MDS (α=0.5), free componentwise Isomap alignment and separation-constrained alignment. The latter imposes ordered positive 2D strips for all K; full cross distances were evaluated afterward, though optimizer placement used 16 spread anchors per component.

## Original one-seed reported measurements

| Rolls K | Points | PCA within | Hybrid within | Component Isomap within (free = separated) | Free cross ambient | Separated cross ambient |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 180 | 0.720 | 0.142 | 0.137 | — | — |
| 2 | 360 | 0.751 | 0.205 | 0.029 | 0.478 | 0.574 |
| 3 | 540 | 0.753 | 0.139 | 0.028 | 0.390 | 0.390 |
| 4 | 720 | 0.750 | 0.096 | 0.035 | 0.315 | 0.303 |
| 5 | 900 | 0.761 | 0.073 | 0.037 | 0.265 | 0.252 |
| 6 | 1,080 | 0.760 | 0.057 | 0.041 | 0.205 | 0.208 |

## Major negative result

At **90 points per roll**, adding the third roll increased the global internal connectivity radius enough to introduce shortcuts and drove intracomponent error up sharply (approximately 0.64 versus 0.14 before). Increasing density to 180 reduced the observed error for this seed but gives **no general guarantee**.

## Algorithmic findings

All K components remained geometrically disjoint in the separated layout, and rigid alignment perturbed computed within-embedding pair distances only at rounding error (~4.3×10⁻¹⁴). Under constrained local optimization, some K=4–5 between stresses were lower than free-fit stresses—this is possible for **different nonconvex local solutions** and does not violate monotonicity of the *global* constrained optimum.

## Interpretation for the paper

A successful visualization of six separated rolls is **not the main contribution**. What matters is quantifying and controlling separation–distortion, verifying an unsupervised radius rule, and comparing a fair Pareto frontier with prior multi-manifold methods. True cross-manifold intrinsic geodesics are not finite. The full original 3D and 2D PNG/SVG galleries still need restoration from the archival ZIP.


## Linked artifacts

- [Code and source status](../../code/008-multiple_swiss_rolls/README.md)
- [Numerical results and provenance](../../results/008-multiple_swiss_rolls/README.md)
- [Summary diagram](../../figures/008-multiple_swiss_rolls/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/008-multiple_swiss_rolls/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.

## Historical summary figure (not a new run)

![Historical experiment 008-multiple_swiss_rolls summary — source-transcribed diagnostic values](../../figures/008-multiple_swiss_rolls/summary.svg)

> This SVG is a reconstructed visualization of historical rounded summaries, not a recovered 3D/2D projection. Actual figures will be embedded automatically under the latest computed run after executing the Conda pipeline.

