# AI handoff — ProximityGraphs-Isomap

**Updated:** 2026-10-18
**Latest history:** [2026-10-18 — EXP-009 official figures verified](proximity_isomap/history/journal/2026-10/2026-10-18-exp009-published.md).

## Canonical structure

- **[Experiment notes](proximity_isomap/notes/README.md)** are the primary scientific record for EXP-001..008, with matching numbered folders in code, figures and results.
- Original historical journal and decisions preserved at [history](proximity_isomap/history/README.md), and mathematics at [notes/mathematics](proximity_isomap/notes/mathematics/index.md). Root legacy journal/context/experiments/figures/results/notes have been consolidated rather than erased.
- Shared scientific Python library remains in `src/proximity_isomap/`. Working paper direction: [separation–distortion frontier](paper/RESEARCH_DIRECTION.md). Originality is **not established**.

## New reconstructed experiments

The current `proximity_isomap/code/research_runner.py` implements **new reconstructions** of EXP-001..008 (radius scan, hybrid MDS, density transfer, separate Swiss/S-curve manifolds, rotated rolls, rigid separation and 1–6 roll panels). The user explicitly rejected importing Integration.zip. Numerical parity with the old original 002–008 algorithms must not be claimed.

The Windows Conda/PowerShell entrypoint is `scripts/run_all.ps1`. The environment pins the user's own [contrastcolors](https://github.com/heri-espino/Colors) package at Git SHA `84e05b40b6ba6aa6864f5bc13ad43da3c4c1e93d`. Every **full** run writes CSV/JSON/NPZ and actual PNG/SVG figures and embeds its newly generated PNG panels into that experiment's Markdown note. Smoke runs are ignored from version control and do not change the notes.

**Run status:** Full experiments have NOT been run on the user's Windows machine during this repository-edit session. CI tests are separate from scientific data generation. Use `./scripts/run_all.ps1 -Quick` to smoke-test and `./scripts/run_all.ps1 -Push` to compute/commit/push full evidence.

## Verified GitHub CI

[Run 39139028489](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39139028489) passed on Python 3.11 and 3.12, including tests, Ruff, structure validators, Sphinx and actual **quick-mode runs for all eight rebuilt experiments using the pinned ContrastColors library**. This is evidence the smoke pipeline executes, **not** evidence of full numerical reproduction on the user's Windows environment or parity with the old original algorithms.

## Upcoming research: TDA filtration + stochastic geometry (proposed 2026-10-18)

**Read:** [VR–random-geometry research brief](proximity_isomap/notes/mathematics/research_tda_stochastic_geometry.md) and [PROP-0003, finite-sample recovery window](proximity_isomap/notes/mathematics/results/PROP-0003-component-recovery-window.md).

- Existing results: β0(VR_r) equals graph component count; MST edge lengths are H0 death events; for known true groups, b=max within-MST bottleneck and δ=min cross-group point distance, and an exact partition radius exists iff b<δ. These statements are elementary, **not new theory**.
- Candidate probabilistic bound: under separated compact connected supports and positive-mass radius-r/4 covering balls, binomial and support-wise Poisson void probabilities yield a union bound on connected-component recovery. Requires strong sampling assumptions; no Isomap geodesic-consistency guarantee follows automatically.
- **Prior art to confront:** M-Isomap, S-Isomap++, supervised MMD-Isomap, TopoMap/TopoMap++ (full 0D VR persistence), DIPOLE (metric + persistent homology), Joint MDS and tuned Isomap. Novelty/predicted superiority not demonstrated.
- Run **EXP-009 only after a documented fair comparison protocol**. Full EXP-001–008 reruns remain on the explicit GitHub to-do issue: https://github.com/heri-espino/ProximityGraphs-Isomap/issues/6. Do not mark them complete because quick CI passed.

**Latest dated history:** [2026-10-18 — stochastic geometry proposal](proximity_isomap/history/journal/2026-10/2026-10-18-tda-stochastic-direction.md).

## Proposed H1 holes and visualization (2026-10-18)

See [TDA stochastic geometry research brief](proximity_isomap/notes/mathematics/research_tda_stochastic_geometry.md). Unlike H0 graph components, H1 must be computed on VR **simplicial complexes**, including filled triangles. Two Swiss-roll strips have no true H1; two circles have two loops. Rigid placement preserves **all** VR persistence of already embedded individual components, but not necessarily the persistence of the original ambient cloud or of the union. Ripser/GUDHI can compute diagrams; representative cocycles and geometric cycles are not interchangeable. Proposed only, no EXP-009 benchmark performed. Future published figures must use ContrastColors.

## EXP-009 topological-manifolds pilot (executed 2026-10-18)

[Experiment note](proximity_isomap/notes/009-topological_manifolds/README.md) and [runnable code](proximity_isomap/code/009-topological_manifolds/run.py). Deterministic 172-point Swiss-roll/cylinder/torus test: K=3 MST-cut partition given the number K recovered the groups; isometric rigid separation preserved independent Isomap distances but did **not** preserve H1 barcodes computed with ambient Euclidean VR before/after embedding (within r<=7). Long H1 counts (lifetime>=1): Swiss 1 to 0, cylinder 1 to 0, torus 9 to 1. The true Betti-1 counts are 0, 1, 2; excess torus and Swiss sample bars are finite-grid artifacts. **GitHub reproducibility verified:** [publication workflow run 39163692726](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39163692726) successfully generated and committed ContrastColors PNG/SVG, coordinates NPZ and full H1 persistence JSON in [run_efbeaad418](proximity_isomap/results/009-topological_manifolds/runs/run_efbeaad418/metrics.json). The experiment note embeds the actual figures. Full 001–008 local reruns remain pending issue #6. Full 001-008 local reruns still pending issue #6.

## Scientific limitations and next work

Radius choices for many disconnected configurations are diagnostic and use known true generating labels; EXP-004 development uses analytic intrinsic truth for choosing a radius multiplier. The hybrid MDS and rigid alignment variants are newly rebuilt approximations of the historical methodology; separation uses a feasible ordered strip heuristic, not a proven globally optimal frontier.

After full local reruns, inspect generated figures and metrics, confirm GitHub CI, report commit SHA, then focus on *unsupervised* radius selection, tuned prior-art comparisons and separation–distortion frontiers. Read [AGENTS.md](AGENTS.md) and follow its mandatory synchronized per-experiment notes/figures/results rules.
