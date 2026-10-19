# EXP-010 — Cylinder sampling versus five disconnected circular rings

> **New local run status:** The native EXP-010 Python code is now committed under `proximity_isomap/code/`. The numbers and derived SVG currently shown below are **previous exploratory pilot summaries**, NOT the result of your upcoming Windows run. After you push the new run's CSV/JSON/NPZ and PNG/SVG files, the assistant will replace this preliminary narrative with a mathematical interpretation grounded in your measured outputs. You do not need to download/import any ZIP.\n\n
**Research status:** completed locally, deterministic exploratory run (2026-10-18). This GitHub note records the mathematics and numerical findings. The full original Python runner, saved point arrays, detailed CSV/JSON, and four PNG/SVG figure pairs remain in the downloadable EXP-010 local ZIP, awaiting a fresh Windows/Conda run. The SVG summary below is derived directly from the locally recorded counts; it is not a substitute for the original projection figures.

## Research question

Does a sampled cylinder contain several connected circles, or is it one connected surface? How do the proximity-graph connected components and the sampled Vietoris–Rips loops change as the radius becomes smaller and the number of observations grows?

The cylinder is C = { (3.1 cos θ, 3.1 sin θ, z) : 0 ≤ θ < 2π, −4 ≤ z ≤ 4 }. We used four deterministic grids with 54, 144, 360 and 720 points. A second sample contains five genuinely disjoint circles at heights −4, −2, 0, 2 and 4, with 90 points on each ring (450 total). The grids are not nested random samples.

## Mathematics

The Euclidean proximity graph has an edge iff ||x_i − x_j||₂ ≤ r. Using the Euclidean minimum spanning tree,

$$
\beta_0(r)=n-\#\{e\in\operatorname{MST}(X):w(e)\le r\}.
$$

For the Vietoris–Rips complex including all triangles, the first Betti number at a *fixed radius* is

$$
\beta_1(r)=|E_r|-n+\beta_0(r)-\operatorname{rank}_{\mathbb F_2}(\partial_2).
$$

This is fixed-scale homology, **not** a computation of every individual persistent birth/death interval. For the ideal support, the cylinder has (β₀,β₁)=(1,1); five disconnected circles have (5,5).

## Measured components

| Dataset | Observations | Entire-sample MST threshold | β₀(0.5) | β₀(1.25) |
|---|---:|---:|---:|---:|
| Cylinder (9×6) | 54 | 2.1205 | 54 | 54 |
| Cylinder (12×12) | 144 | 1.6047 | 144 | 12 |
| Cylinder (18×20) | 360 | 1.0766 | 18 | **1** |
| Cylinder (24×30) | 720 | 0.8093 | 24 | **1** |
| Five rings (5×90) | 450 | 2.0000 | **5** | **5** |

For the 360-point cylinder, at radius 1.15 the sampled VR complex had β₀=1 and β₁=343; by radius 1.25 these values were β₀=1 and β₁=1. The 343 transient grid cycles are not 343 holes in the continuous cylinder. The separate rings retained β₀=5 and β₁=5 through the tested interval 0.25–1.80; they begin merging at their 2-unit vertical separation.

![Observed component-count comparison (summary of local numerical results)](../../figures/010-radius_density_and_rings/summary.svg)

## Original 3D and 2D figures

The executed local experiment generated geometry.png, radius_topology.png, radius_snapshots.png and projections.png **and matching SVGs**. Its original complete Markdown note embeds those actual images. They belong under:

proximity_isomap/figures/010-radius_density_and_rings/runs/20261018-exploratory/

Corresponding results include fixed_scale_betti.csv, beta0_curve.csv, summary.csv, metrics.json, observations.npz and sha256.json. Runner: proximity_isomap/code/010-radius_density_and_rings/run.py.

**Full GitHub publication is pending the fresh user-run output publication.** Use scripts/run_exp_010_011.ps1 after downloading the EXP-010 and EXP-011 ZIPs. The importer replaces this provisional note with the original complete illustrated note.

## Limitations

Deterministic regular grids can generate spurious VR cycles and do not establish probabilistic manifold recovery. Lowering radius too far fragments the finite sample; it does not turn a continuous cylinder into several genuinely disconnected rings. Independent Isomap projections do not automatically preserve original Euclidean VR persistence.
