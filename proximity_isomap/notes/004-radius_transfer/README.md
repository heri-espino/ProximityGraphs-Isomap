# EXP-004 — Radius transfer to new manifolds and sampling densities

**Research question.** Can a radius chosen on uniform Swiss rolls generalize to different point densities and another manifold family?

## Design

A fixed 50-point grid combines broad logarithmic radii with denser candidates near the low-error region. Select the global scale multiplier using **10 development uniformly sampled Swiss rolls only**; evaluate the chosen radius on **32 independent datasets**: 8 each for Swiss/uniform, Swiss/skewed, S-curve/uniform and S-curve/skewed. Ninety observations per dataset. The tested development-selected multiplier was ρ≈0.984 times the observed median tenth-neighbor distance. One optimization initialization and α=0.5.

## Historical reported means (within-manifold intrinsic stress; lower is better)

| Evaluation regime | Hybrid | PCA | kNN Isomap (k=10) |
|---|---:|---:|---:|
| Swiss/uniform | 0.560 | 0.731 | 0.690 |
| Swiss/skewed | 0.405 | 0.483 | **0.355** |
| S-curve/uniform | **0.203** | 0.285 | 0.221 |
| S-curve/skewed | 0.140 | 0.164 | **0.102** |

## Findings, interpretation and limitations

The selected global radius did **not** uniformly beat kNN Isomap. All eight skewed Swiss-roll graphs were still disconnected at the selected radius. Descriptive best-in-sample radii tended to be larger when sampling was skewed; those individual best radii are **post-hoc oracle diagnostics**, not fair selection scores. This motivated a possible density-aware or per-point radius—not yet validated. The comparison uses only one fixed kNN setting, not a tuned competitor.

## Failed or incomplete work

The initial long run was interrupted before final CSV writing. A newer local runner introduced per-dataset atomic checkpoints and a config hash, but those source and checkpoint files are not on GitHub main.

## Next question

Investigate whether componentwise geometry can still be preserved on **two genuinely disjoint** surfaces, with placement evaluated separately (EXP-005).


## Linked artifacts

- [Code and source status](../../code/004-radius_transfer/README.md)
- [Numerical results and provenance](../../results/004-radius_transfer/README.md)
- [Summary diagram](../../figures/004-radius_transfer/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/004-radius_transfer/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.
