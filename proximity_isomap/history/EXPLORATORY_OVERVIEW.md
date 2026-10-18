# Exploratory numerical results (historical EXP-0002–0008 archives)

**Status:** Directly recorded summaries transcribed from local research CSVs; not independent reruns of the historical experiments. Full source, CSV/JSON/NPZ arrays and figures have been reconciled into a 260-file import bundle but **have not yet been pushed to GitHub**. See [import status](../experiments/ARCHIVE_INTEGRATION_STATUS.md) and journal entry [2026-10-17 — numerical summaries](../journal/2026-10/2026-10-17-archived-numerical-summaries.md).

## Why the experiments evolved

EXP-0002 compared PCA, kNN Isomap, radius Isomap and hybrid weighted MDS on an initial Swiss roll. A disconnected graph stitched using ambient distances could severely distort intrinsic distances. EXP-0003 widened the radius grid from almost isolated points to complete graphs and identified abrupt changes near connectivity transitions. These early experiments were exploratory and cannot justify an oracle radius selector.

EXP-0004 tested fixed-radius transfer. Ten uniform-Swiss-roll development samples selected a dimensionless radius around 0.984 times the median tenth-neighbor distance; results below are means over eight independently sampled evaluation datasets per condition (lower stress is better).

| Evaluation geometry | Hybrid MDS | PCA | kNN Isomap k=10 |
|---|---:|---:|---:|
| Swiss roll, uniform density | 0.560 | 0.731 | 0.690 |
| Swiss roll, skewed density | 0.405 | 0.483 | **0.355** |
| S-curve, uniform density | **0.203** | 0.285 | 0.221 |
| S-curve, skewed density | 0.140 | 0.163 | **0.102** |

This mixed result suggests a global radius may fail under sampling-density shift; no universal win is established.

EXP-0005 used two disconnected Swiss rolls and two disconnected S-curves. For separate underlying manifolds, **intrinsic geodesics between the manifolds are not finite**. Evaluate within-manifold intrinsic stress separately from between-manifold original Euclidean placement stress. EXP-0006 rotated one Swiss roll (360 total points) across four paired seeds, making a common PCA plane less satisfactory; this does not replace a well-tuned Isomap baseline.

## EXP-0007: four independent rotated two-roll samples

Mean normalized stress (lower is better; original cross-manifold distances are ambient Euclidean):

| Method | Within-roll intrinsic stress | Between-roll ambient stress |
|---|---:|---:|
| PCA | 0.7646 | **0.0420** |
| Global hybrid MDS | 0.2455 | 0.2338 |
| Componentwise Isomap, free alignment | **0.0891** | 0.5584 |
| Componentwise Isomap, separated alignment | **0.0891** | 0.7120 |

The componentwise rigid transformations preserve internal *computed* Isomap distances; spatial non-overlap costs additional cross-manifold ambient fidelity in this sample.

## EXP-0008: one through six rotated Swiss rolls

One synthetic realization per roll count, **180 observations per roll**; diagnostic radius selected using known true sheet identities, not unsupervised optimization. Normalized *within-roll intrinsic* stress (lower is better):

| Number of rolls | PCA | Global hybrid MDS | Separated componentwise Isomap |
|---:|---:|---:|---:|
| 1 | 0.720 | 0.142 | 0.137 |
| 2 | 0.751 | 0.205 | 0.029 |
| 3 | 0.753 | 0.139 | 0.028 |
| 4 | 0.750 | 0.096 | 0.035 |
| 5 | 0.761 | 0.073 | 0.037 |
| 6 | 0.760 | 0.057 | 0.041 |

For six rolls, between-roll ambient stress was 0.205 with free alignment and 0.208 with enforced separated alignment. Ordered non-overlapping strips were achieved; a pilot with only 90 points per roll showed a severe shortcut problem, so the 180-point results are not general guarantees.

## Mandatory qualifications

- Components discovered by radius graphs may not equal true disconnected manifolds. Some exploratory experiments **used oracle generating sheet labels to choose radii**, not merely to score the results.
- Local nonconvex optimizers, incomplete tuning, limited seeds, and differences in graph edge densities limit the validity of claims of superiority.
- Stress against graph-derived distances is not the same as stress against the true manifold metric; cross-manifold ambient distances are an intentionally different target.
- These tables do not demonstrate novelty. [paper/RESEARCH_DIRECTION.md](../paper/RESEARCH_DIRECTION.md) remains the provisional thesis.
- Numeric values are rounded from the original archived CSV files; publication claims require importing those files, verifying per-run metadata, and repeating the analyses under a pinned Git SHA and environment.
