# 2026-10-18 — Propose Vietoris–Rips and random-geometric-graph theory for Isomap

**Status:** Literature-informed proposal and elementary derived result; no new numerical experiment.

## Motivation

The user requested that runnable full EXP-001–008 reconstructions remain a pending to-do and suggested comparing with multi-manifold Isomap while using Vietoris–Rips filtration and binomial/Poisson point process models for stronger geometry and probability guarantees.

## Work documented

- Opened an explicit GitHub task for the pending **full** local Conda/ContrastColors 001–008 reruns: https://github.com/heri-espino/ProximityGraphs-Isomap/issues/6. Prior CI quick smoke passes do not complete it; `Integration.zip` remains excluded.
- Added `PROP-0003`: for known generating groups, the exact sampled-component recovery window is `b ≤ r < δ` iff `b<δ`, with a sufficient perturbed-margin condition `δ−b>4ε` for matched ε-perturbed points.
- Added a new mathematical workstream explaining β0(VR_r)=component count; finite H0 merge times = MST edges, and elementary high-probability sampling bounds by covering/void events for binomial and manifold-supported Poisson samples.
- Named **EXP-009 as proposed, not executed**, and set a competing-methods list: M-Isomap, S-Isomap++, supervised MMD-Isomap, TopoMap/TopoMap++, DIPOLE, Joint MDS, tuned Isomap and PCA.
- Updated canonical NEXT_STEPS, math index, AI_HANDOFF, context STATE and working paper thesis without changing numerical source code or any existing experimental artifact.

## Critical prior art and interpretation

TopoMap preserves *all* zero-dimensional Vietoris–Rips persistence, and DIPOLE uses metric + persistence learning. Penrose's random geometric graph theory and Bobrowski–Kahle random geometric complex survey cover stochastic graph topology. Neither persistence nor basic random-graph connectivity properties are new. The opportunity, **unproved**, is a calibrated unsupervised radius selector integrated with intrinsic Isomap and an explicit separation–placement-distortion frontier, with fair baselines and possible finite-sample guarantees.

No PDF theorem text was imported into the literature corpus by this note: external source pointers are registered as a **reading queue**, not a completed source-verified novelty matrix. Do not assert mathematical novelty.

## Next

Run full EXP-001–008 later from Windows PowerShell and close the pending issue only after inspecting results and GitHub CI. Independently verify baseline papers and design EXP-009 with binomial/Poisson sampling, sparse folds, varying gaps and negative cases (crossings/unequal densities), using generating labels only in evaluation.
