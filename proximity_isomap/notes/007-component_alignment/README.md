# EXP-007 — Unfold graph components independently, then rigidly separate

**Research question.** Why did disconnected Swiss-roll projections cross, and can we guarantee non-overlap without re-distorting each separately unfolded roll?

## Algorithm

1. Build a radius graph with exactly two connected components.
2. Compute shortest paths **inside each component**, then classical MDS (Isomap) independently.
3. Solve for each component's planar rotation and translation to approximate **original ambient cross-component Euclidean distances**.
4. Compare free alignment with a **positive x-coordinate hull gap**; allow both components to rotate before imposing the gap.

Rigid alignment leaves distances of the **computed independent embeddings** unchanged, even though they may not exactly equal the true intrinsic geodesics. The strip constraint makes both projected convex hulls disjoint.

## Four-seed means on rotated 360-point paired Swiss rolls

| Method | Within-sheet intrinsic stress | Between-sheet ambient stress |
|---|---:|---:|
| PCA | 0.7646 | **0.0420** |
| Global hybrid MDS | 0.2455 | 0.2338 |
| Componentwise Isomap + free alignment | **0.0891** | 0.5584 |
| Componentwise Isomap + positive separation | **0.0891** | 0.7120 |

## Failure and correction

The first attempt kept component 1 horizontally fixed and forced large displacement along x, with very high between stress (approximately 1.06 on one rotated seed). Allowing **both** components to rotate reduced that particular error substantially. This records a real abandoned design, not a result to hide.

## Interpretation and limitations

Non-overlap was guaranteed, and internal computed distances were preserved to floating-point precision. But the guarantee can increase relative-placement distortion. These are tradeoffs, not dominance claims. The method was originally implemented for **exactly two** components and used a label-informed diagnostic radius. EXP-008 generalizes to K components.


## Linked artifacts

- [Code and source status](../../code/007-component_alignment/README.md)
- [Numerical results and provenance](../../results/007-component_alignment/README.md)
- [Summary diagram](../../figures/007-component_alignment/summary.svg) — redrawn from reported values, not an original experimental screenshot
- [Figure directory and original-plot status](../../figures/007-component_alignment/README.md)

**Research status:** Exploratory and historical. Full EXP-002–EXP-008 source, 3D projections, raw arrays and original figure artifacts remain outside GitHub until the cumulative ZIP is imported. Do not claim reproduced results from current main.
