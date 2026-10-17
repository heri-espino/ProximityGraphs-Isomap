# Next steps (ordered)

**Updated:** 2026-10-16

- [ ] Run **Ruff and Sphinx** on a connected environment/CI; local sandbox passed 16 tests and structural checks but could not download the missing development dependencies. Capture exact environment versions in first run metadata.
- [ ] Import primary-source PDFs in `literature/pdf/`, extract Markdown using Docling into `literature/markdown/`, and verify page-specific key results in `literature/references/`. Record one entry per source in `MANIFEST.csv` and verified theorems in `KEY_RESULTS.md`.
- [ ] Conduct a targeted novelty review of disconnected Isomap, landmark and joint/weighted MDS, manifold stitching, and graph-based geodesic approximation; cite verified source entries from `literature/references/`.
- [ ] Implement *standard* Isomap and Euclidean MDS baselines with consistent shortest-path conventions and disconnected behavior.
- [ ] Specify and implement hybrid weighted MDS optimization with numerical checks (objective decreases, gradient check, multistart, disconnected edge cases).
- [ ] Specify and implement componentwise embedding plus rigid alignment; document rotational, translational and reflection ambiguities.
- [ ] Decide how to select `r`, output dimension `d`, and mixing parameter `alpha` **without looking at evaluation targets**.
- [ ] Create EXP-0002 for held-out comparisons and ensure all methods use the same samples/seeds.
- [ ] Select project license only after explicit author decision.

## Definition of done for the first scientific milestone

A fixed, reproducible comparison on synthetic manifolds with known intrinsic distances; strong PCA/MDS/Isomap baselines; component-count and runtime reporting; normalized in/out stress reported separately; and a negative-results section.
