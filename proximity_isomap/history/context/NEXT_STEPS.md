# Next steps — 2026-10-19

## Completed checkpoint

- [x] User generated and pushed full numerical/visual EXP-010 and EXP-011 run 20261019T061001Z-full.
- [x] Assistant reviewed actual CSV/metadata, UMAP availability and versioned figure paths; appended computed-run scientific results with 4 and 8 actual PNG figures.
- [x] Expand checkpoint-012 main Marp with mathematical explanations and published EXP-010/011 galleries.
- [x] Create **standalone 53-slide Marp mathematical lecture** deriving componentwise kNN-Isomap in detail (MDS, geodesics, component discovery, rigids, constrained placement, metrics, complexity).
- [ ] On user's Windows machine, render and visually inspect lecture PDF/PPTX and presentation PDF for equation/table overflow.

## Proposed EXP-013 specialized kNN study (NOT RUN)

- [ ] Assistant: implement and commit the *new* experiment code, tests and matching preliminary mathematical/figure plan under numbered 013 folders. Do not claim completed results.
- [ ] Sweep k_detect and k_embed separately; inspect per-dataset component recovery (evaluation labels only), connected local graphs and failure/bridge modes.
- [ ] Add within-geodesic stress, local trustworthiness, ambient centroid/cross stress, hull-clearance violations, runtimes, sample-density/noise and random seeds.
- [ ] Evaluate simple separated strips independently from centroid/landmark-constrained optimized placement; distinguish proposed solver from guaranteed optimum.
- [ ] User: execute full EXP-013 on Windows, verify and push generated CSV/JSON/NPZ and PNG/SVG.
- [ ] Assistant: read the exact EXP-013 outputs, append computed-run mathematical interpretation and real images to 013 notes, then update checkpoint 012.

## Scientific controls

- [ ] Literature novelty matrix against source-verified D-C Isomap, M-Isomap, S-Isomap++, TopoMap, DIPOLE and metric-constrained alignments.
- [ ] Perform multiple-seed and independent-confirmation tests; do not infer general superiority from the one-seed EXP-011.


## EXP-013: immediate user-run task (not completed yet)

- [x] Commit code, local Windows runner, regression tests, numbered notes and planned figure manifest for classical multi-manifold far/near dashboards.
- [x] Expand the shared Marp lecture with both 3x3 dashboard definitions, sampled-distance construction, method caveats, mathematical and open-question sections; no ungenerated image links.
- [ ] User: `git pull --ff-only`, install real `umap-learn` if needed, run `python -m pytest tests/test_exp013_classical_dashboards.py -q`, then `./scripts/run_exp_013.ps1 -Quick` (PowerShell invocation with backslash) and `./scripts/run_exp_013.ps1 -RequireUmap -Push`.
- [ ] Assistant: after the user pushes, inspect full method_metrics, K recovery, k grid, 28 real dashboards and errors. Write 013 mathematical results and embed real figures in both EXP-013 notes and lecture checkpoint 012. Do not declare the new experiment measured until this occurs.
- [ ] Follow up: rerun multiple seeds and vary near/far closeness for statistical confirmation; compare optimized placement and stronger published multi-manifold methods in a separate future experiment.
