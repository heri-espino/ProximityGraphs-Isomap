# 2026-10-18 — Versioned EXP-009 ContrastColors figures published

**Evidence:** [GitHub Actions run 39163692726](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39163692726) succeeded on source commit `efbeaad418a7f4e6a6aab2038ba6b1bdad5d5baf`, producing data under immutable run label `run_efbeaad418`.

**Assets committed:** original 3D/PCA/separated 2D views in PNG and SVG; original-versus-2D sampled VR H1 barcode panels in PNG and SVG; `coordinates.npz` and full per-manifold persistence pairs plus run metadata in `metrics.json`. All figures generated with the user's pinned ContrastColors library, using the `heri` style and Okabe–Ito palette. They are embedded and linked in the EXP-009 Markdown note.

**Scientific outcome:** On 172 deterministically gridded points, the supplied K=3 MST cut recovered the correct three graph components. The H1 comparison exhibits false positives on a finite sampled Swiss roll and torus and a missing prominent cylinder H1 bar in its 2D Isomap representation under r<=7. This is a pilot; topology and embedding success cannot be generalized to random point processes or unsupervised selection.

**Remaining tasks:** Expand across random binomial and Poisson samples and independent seeds; compare TopoMap and DIPOLE, assess graph shortcuts and true intrinsic metrics, and keep historical full EXP-001–008 runs pending. The commit is a scientific recording of a negative diagnostic, not a publishable novelty result.
