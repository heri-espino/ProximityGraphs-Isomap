# AI handoff — ProximityGraphs-Isomap

**Updated:** 2026-10-18
**Latest history:** [2026-10-18 — Verified reconstructed experiment smoke tests](proximity_isomap/history/journal/2026-10/2026-10-18-smoke-ci-verified.md).

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

## Scientific limitations and next work

Radius choices for many disconnected configurations are diagnostic and use known true generating labels; EXP-004 development uses analytic intrinsic truth for choosing a radius multiplier. The hybrid MDS and rigid alignment variants are newly rebuilt approximations of the historical methodology; separation uses a feasible ordered strip heuristic, not a proven globally optimal frontier.

After full local reruns, inspect generated figures and metrics, confirm GitHub CI, report commit SHA, then focus on *unsupervised* radius selection, tuned prior-art comparisons and separation–distortion frontiers. Read [AGENTS.md](AGENTS.md) and follow its mandatory synchronized per-experiment notes/figures/results rules.
