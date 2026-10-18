# Next steps (ordered)

**Updated:** 2026-10-17 (working paper thesis adopted)

- [ ] Create the Conda environment with `conda env create -f environment.yml`, activate it, test installation, and rerun EXP-0001 from a Git checkout with SHA and `conda list --explicit` archived.
- [x] Confirmed GitHub Actions run 38997728144 on Python 3.11/3.12: 16 tests, Ruff, integrity validation, Sphinx all passed for commit `e7cc9bc`.
- [x] **Ruff and Sphinx passed in pip-based GitHub CI** (run 38997728144, Python 3.11/3.12). Conda solving and Conda-based EXP-0001 remain unverified; capture environment versions in the first Conda run.
- [ ] Import primary-source PDFs in `literature/pdf/`, extract Markdown using Docling into `literature/markdown/`, and verify page-specific key results in `literature/references/`. Record one entry per source in `MANIFEST.csv` and verified theorems in `KEY_RESULTS.md`.
- [ ] Conduct a targeted novelty review of disconnected Isomap, landmark and joint/weighted MDS, manifold stitching, and graph-based geodesic approximation; cite verified source entries from `literature/references/`.
- [ ] Implement *standard* Isomap and Euclidean MDS baselines with consistent shortest-path conventions and disconnected behavior.
- [ ] Specify and implement hybrid weighted MDS optimization with numerical checks (objective decreases, gradient check, multistart, disconnected edge cases).
- [ ] Specify and implement componentwise embedding plus rigid alignment; document rotational, translational and reflection ambiguities.
- [ ] Decide how to select `r`, output dimension `d`, and mixing parameter `alpha` **without looking at evaluation targets**.
- [ ] Create EXP-0002 for held-out comparisons and ensure all methods use the same samples/seeds.
- [ ] Select project license only after explicit author decision.

## 2026-10-17 — Paper-specific priorities

- [x] Record the separation–distortion research thesis, proposed optimization and candidate paper structure in [paper/RESEARCH_DIRECTION.md](../paper/RESEARCH_DIRECTION.md); record the decision in ADR-0005.
- [ ] Verify overlap with multi-manifold Isomap, manifold stitching, weighted/joint MDS, discriminant approaches and geometric separation constraints, with primary PDFs and theorem-level annotations.
- [ ] Reconcile EXP-0002–EXP-0008 local ZIP experiments/code/plots with remote main without losing CI/Conda changes; record a Git SHA and test the integrated implementation.
- [ ] Replace label-informed graph construction/radius selection with a real unsupervised approach; quantify incorrect connected-component merges/splits.
- [ ] Compare normalized hull-separation versus cross-ambient-distortion frontiers across independent seeds with a competitive tuned baseline; preserve computed intracomponent embedding distances.
- [ ] Establish a substantive theoretical or methodological advantage before claiming novelty in paper text.

## Definition of done for the first scientific milestone

A fixed, reproducible comparison on synthetic manifolds with known intrinsic distances; strong PCA/MDS/Isomap baselines; component-count and runtime reporting; normalized in/out stress reported separately; and a negative-results section.
