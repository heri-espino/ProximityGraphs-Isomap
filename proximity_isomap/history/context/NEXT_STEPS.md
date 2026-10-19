# Next steps (2026-10-18)

## Prepared explanatory notes — DONE, new figure generation still pending

- [x] Add dedicated mathematical definitions/objectives to the nine numbered experiment notes.
- [x] Add labeled figure plans rather than broken future-image links; preserve existing historical SVG and the actual EXP-009 PNG/SVG.
- [x] Update runner and validation rules to preserve **all** future documented runs rather than overwrite previous run descriptions.

## Pending full EXP-001–008 reruns — NOT DONE

**GitHub tracking issue:** https://github.com/heri-espino/ProximityGraphs-Isomap/issues/6

- [ ] In a Conda-enabled Windows PowerShell checkout, run `./scripts/run_all.ps1 -Quick`.
- [ ] After inspection, run `./scripts/run_all.ps1 -Push` to generate **full** 001–008 CSV/JSON/NPZ, PNG/SVG and Markdown images with pinned ContrastColors.
- [ ] Inspect every figure/metric, verify push SHA and CI, then mark the issue complete. Never import `Integration.zip` or confuse CI smoke passes with full research runs.

## New theoretical / benchmarking workstream — proposed

- [ ] Read [TDA + random geometry research brief](../../notes/mathematics/research_tda_stochastic_geometry.md) and [finite-sample recovery window](../../notes/mathematics/results/PROP-0003-component-recovery-window.md).
- [ ] Prepare source-verified novelty matrix against M-Isomap, S-Isomap++, supervised MMD-Isomap, TopoMap/TopoMap++, DIPOLE, Joint MDS, and tuned standard Isomap.
- [ ] Design unsupervised 0D persistence/MST-based radius calibration **without true generating labels**; distinguish full H0 persistence from fixed-radius separation.
- [ ] Derive/test binomial- and Poisson-sampling recovery probabilities, including unequal densities, sparse folds, perturbations and intersecting supports.
- [ ] Expand the executed EXP-009 pilot into matched baselines and stochastic VR-filtration experiments; do not create numerical claims before executing it.


- [x] Consolidate legacy folders into `proximity_isomap/history` and move math notes to experiment research area without deleting archived text.
- [x] Rebuild new experimental scripts and PowerShell runner with pinned ContrastColors.
- [x] Embed existing historical SVG summaries into all eight notes.
- [ ] In Conda PowerShell: `./scripts/run_all.ps1 -Quick` and inspect smoke behavior.
- [ ] From a clean branch: `./scripts/run_all.ps1 -Push` for full 001–008 new runs, images, NPZ, CSV, JSON and Markdown updates; then verify GitHub CI and log the commit SHA.
- [ ] Compare code-generated numbers to historical summaries as an **implementation difference study**, not equality.
- [ ] Add unsupervised radius selection and run independently seeded margin–distortion frontiers with tuned prior-art methods.

- [ ] Extend proposed EXP-009 topology diagnostics to H1 loops (and optionally H2 cavities): VR triangles, persistence barcodes, representatives, original-vs-projection metrics, with ContrastColors figures embedded in Markdown. This is not a completed run.


## Professor presentation

- [x] Author professor-facing Marp presentation with mathematics, metric definitions, measured tradeoffs and all current GitHub versioned experimental figures.
- [ ] Inspect the Marp PDF/PPTX export visually on the user's machine; this connector session did not run the browser renderer.
- [ ] Integrate and rerun EXP-010/011 locally generated figures in GitHub, then extend the slide atlas.


## Mandatory publication of EXP-010 and EXP-011

- [x] Record experiments 010/011 as scientific Markdown notes and derived summary SVGs on GitHub; move Marp presentation to 012.
- [x] Add GitHub completion gate to AGENTS.md and a safe original-ZIP importer.
- [ ] User: download both original EXP-010/011 ZIPs, run `scripts/import_exp010_exp011.ps1 -Push`, then verify original code, metrics, 3D/2D PNG/SVG and mathematical notes render on GitHub.
- [ ] Execute genuine UMAP on a new run and update 011, without overwriting the exploratory run.


## Active: native EXP-010 and EXP-011 reruns

- [x] Commit code and Windows runner directly to GitHub; remove ZIP dependency.
- [ ] User runs `scripts/run_exp_010_011.ps1 -Quick` followed by `scripts/run_exp_010_011.ps1 -RequireUmap` and pushes fresh immutable CSV/NPZ/JSON and PNG/SVG artifacts.
- [ ] Assistant reviews the **new user-run evidence**, interprets and updates the full 010/011 mathematical Markdown notes with actual embedded figures and refreshes checkpoint 012 Marp.
- [ ] Reconcile differences from the previous one-seed exploratory pilot; do not silently combine metric definitions or results from different implementations.
