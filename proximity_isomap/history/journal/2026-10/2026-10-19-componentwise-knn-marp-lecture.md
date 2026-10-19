# 2026-10-19 — Componentwise kNN-Isomap mathematical lecture and executed evidence

## Request

The user asked to create the specialized algorithm presentation as a Markdown (Marp) class with substantial mathematical exposition, building from the componentwise kNN-Isomap comparison.

## Source checks

The GitHub main branch now contains the user's actually executed EXP-010 and EXP-011 full run 20261019T061001Z-full, including true UMAP records, original PNG/SVG and CSV/NPZ/metadata. Measurements were read from the actual CSV; image paths were checked against the GitHub recursive tree.

EXP-010 computes radius-dependent graph components and fixed-scale VR H1 for a sampled cylinder and five separate rings. The cylinder can temporarily show 343 grid-induced sampled loops at radius 1.15 before H1=1 at radius 1.25; this is not 343 support holes.

EXP-011 reports componentwise kNN Isomap stress 0.245 for five rings with zero hull overlaps, compared to global Isomap k=24 stress 0.250 with all ten hull pairs intersecting. However, the componentwise strip placement has poor ring centroid stress 2.311 vs PCA 0.414. UMAP is genuinely installed and executed; trustworthiness ~1.0 on rings while centroid stress is ~6.263. Componentwise kNN does not dominate the Swiss-roll pair.

## Authored artifacts

- Standalone 53-slide Marp: proximity_isomap/notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md. Teaches symmetrized kNN, two neighborhood parameters, connectivity monotonicity, graph shortest paths, double-centering Gram derivation, strain versus raw stress, positive eigendecomposition, rigid distance-preservation proof, hull clearance, centroid orientation nonidentifiability, landmark stress, frontier, metrics, complexity, topology and failure modes.
- Main checkpoint 012 updated with eight mathematical explanation slides and all twelve actual 010/011 PNG panels; earlier historical figure atlas retained.
- EXP-010 and EXP-011 Markdown notes updated with measured data, limitations, negative findings and original embedded PNG figures.
- Updated presentation README, notes index, AGENTS-prescribed handoff/current state/next steps.

## Distinguish measured from proposed

The executed EXP-011 uses radius/MST (partly supplied K) to detect components, **then** symmetrized 10-NN to calculate graph geodesics within each. It is not yet fully kNN-based unsupervised component recovery. The new EXP-013 detection/embedding k grid and constrained centroid/landmark placement are proposals only; no new EXP-013 numerical results were generated.

## Verification and pending

Every new Markdown image link was checked against available versioned GitHub files. Numerical results reflect the actual CSV and metadata. The Marp PDF/PPTX/browser export, pytest, Ruff, Sphinx and local experiment runs were not executed in this documentation task. A visual slide overflow review remains necessary. The next task may be to implement EXP-013 native code, after which the user runs it locally.
