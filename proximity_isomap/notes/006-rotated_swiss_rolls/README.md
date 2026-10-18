# EXP-006 — Rotated Swiss-roll pair to challenge PCA

**Research question.** Did two parallel rolls make PCA artificially strong? What happens if we retain the same points but rotate the second roll?

## Design

Two Swiss rolls with **180 points each**, 360 observations total. Pair each unchanged original configuration with a second roll rotated **80° about x then 65° about z**, and reposition it by the same gap rule. Four paired seeds, 20261017–20261020. Rigid rotation preserves the intrinsic metric of each roll. Compare global PCA, connected kNN Isomap (fixed k=36) and hybrid MDS (fixed α=0.5) at a synthetic-label-informed two-component radius.

## Four-seed historical means

| Method | Parallel within stress | Rotated within stress | Rotated between ambient stress |
|---|---:|---:|---:|
| PCA | 0.7394 | 0.7646 | **0.0420** |
| kNN Isomap (k=36) | 0.7349 | 0.7504 | 0.0799 |
| Hybrid MDS | **0.2577** | **0.2455** | 0.2338 |

## Interpretation

Rotating a roll makes the shared PCA plane less suited to both nonlinear surfaces, but the hybrid result recovers internal distances at the cost of worse between-roll placement. In the original 2D hybrid projection, **two graph-disconnected rolls visibly formed a cross**. That did not make them connected in the graph: the objective lacked a *geometric non-overlap constraint*. The crossing directly motivated EXP-007.

## Important qualifications

One kNN neighborhood value was not fairly tuned; the diagnostic radius was obtained from known generating sheet identities; and four seeds with a single optimizer start are exploratory only. Pose and horizontal shift changed together to preserve the separation regime.


## Linked artifacts

- [Code and source status](../../code/006-rotated_swiss_rolls/README.md)
- [Numerical results and provenance](../../results/006-rotated_swiss_rolls/README.md)
- [Summary diagram](../../figures/006-rotated_swiss_rolls/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/006-rotated_swiss_rolls/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.
