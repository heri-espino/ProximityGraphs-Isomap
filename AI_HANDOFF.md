# AI handoff — ProximityGraphs-Isomap

**Updated: 2026-10-18.** [Latest dated journal entry](proximity_isomap/history/journal/2026-10/2026-10-18-user-runs-assistant-interprets.md). [Experiment index](proximity_isomap/notes/README.md). Read [AGENTS.md](AGENTS.md) first.

## Mandatory ownership and publication sequence

1. **Assistant:** create tested runnable research code and a pre-run math/figure plan under `proximity_isomap/`, then push source to GitHub. Never send a ZIP instead of a repository update.
2. **User:** run the experiment using the user's Windows Conda environment; produce new immutable CSV/JSON/NPZ and actual PNG/SVG in matching numbered folders; push the generated artifacts.
3. **Assistant:** inspect the precise new runs on GitHub, interpret metrics/plots including failures, write detailed mathematical Markdown notes embedding real figures, update the Marp presentation and history. Never claim a new experimental result without examining the user's generated files.

The current launcher is `scripts/run_exp_010_011.ps1`. **The older ZIP importer is obsolete and has been deleted. Ruff is not required to execute experiments.** Heavy science is local/manual, never on ordinary git push.

## Canonical repository state

- EXP-001–008 are *new reconstructions*, not recovered original historical ZIP experiments. Full versioned PNG/SVG and CSV evidence exists for local run `manual-full-20261018`; note historical and rebuilt output differences.
- EXP-009 is a computed 172-point Swiss-roll, cylinder and torus **pilot**, with the number \(K=3\) supplied. It demonstrated that rigid separation preserves computed distances but cannot recover VR H1 features lost during Isomap embedding.
- **EXP-010:** radius/density, connected cylinder versus five independent rings. Native source: [run.py](proximity_isomap/code/010-radius_density_and_rings/run.py). Its GitHub summary SVG is a **previous exploratory pilot**, not a new user-machine run. Fresh run is pending.
- **EXP-011:** global Isomap and componentwise kNN/radius Isomap compared with PCA, t-SNE and actual optional UMAP. Native source: [run.py](proximity_isomap/code/011-isomap_baselines/run.py). It reports both within-manifold metric error and across-manifold placement, trustworthiness, convex-hull overlaps and graph-bridging diagnostics. Its existing numerical summaries likewise describe a **previous pilot**. The new user run is pending.
- **Checkpoint 012:** [Marp professor presentation](proximity_isomap/notes/012-presentation_checkpoint/README.md). Its original 001–009 versioned image atlas is valid; the added 010/011 charts are prior-pilot *summary SVGs*. Update with the user's actual newly pushed figures after execution.
- Mathematical theory: [stochastic geometry + topology](proximity_isomap/notes/mathematics/research_tda_stochastic_geometry.md), [finite-sample component-recovery radius window](proximity_isomap/notes/mathematics/results/PROP-0003-component-recovery-window.md).
- Working paper question: [separation-constrained Isomap](paper/RESEARCH_DIRECTION.md), optimizing relative intercomponent placement subject to positive projected hull clearance while preserving independently computed internal Isomap distances.

## Scientific validity

Rigid motions exactly preserve within-component computed pairwise distances, **not** original manifold geodesics. Cross-manifold *intrinsic* geodesic distances are undefined/infinite for disconnected supports; evaluate relative arrangement using ambient original intercomponent distances. The proposed frontier is not a confirmed novel theorem; prior work includes D-C Isomap, M-Isomap, S-Isomap++, TopoMap/TopoMap++ and DIPOLE. Synthetic known labels or supplied K in diagnostics do not constitute an unsupervised selector. Do not obscure negative findings, including worsening ambient placement stress under forced separation.

## Immediate actions

**Waiting on user:** 
`git pull --ff-only` then install `umap-learn` if desired, run `scripts/run_exp_010_011.ps1 -Quick` then `scripts/run_exp_010_011.ps1 -RequireUmap`, inspect and `git add/commit/push` full-run results and figures.

**After the push:** locate the exact run IDs, inspect `metrics.csv`, `metadata.json`, saved arrays and all PNG/SVG; update the 010/011 notes with computations, tables, mathematical interpretation, actual inline images and method limitations. Refresh checkpoint 012 and the journal, then verify the remote commit.
