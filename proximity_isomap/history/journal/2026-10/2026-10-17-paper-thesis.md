# 2026-10-17 — Define the separation–distortion paper thesis

**Status:** Manuscript research direction recorded; no numerical experiment run in this change.

## Objective and context

After exploring one through six rotated Swiss rolls in earlier local ZIP experiments, focus the project on a concise publishable method rather than expanding the synthetic gallery. The user specifically proposed four linked aims: unsupervised components, independent intracomponent geometry, guaranteed separation and an explicit metric/framework controlling the distortion cost of that separation.

## Changes and rationale

- Added paper/RESEARCH_DIRECTION.md as the canonical working thesis, including definitions, constrained optimization, evaluation axes, potential novelty, failure criteria and two-figure manuscript plan.
- Revised paper/main.tex and its three sections from a generic disconnected-Isomap outline to a compact separation–distortion formulation. The material is clearly labeled *proposed*.
- Added notes/results/PROP-0002-rigid-separation-frontier.md proving elementary distance invariance, strip separation and nested-feasible-set monotonicity, without calling them original results.
- Added ADR-0005 and registered it in the decision index.
- Updated journal/LATEST.md, AI_HANDOFF.md and context/STATE.md/NEXT_STEPS.md to preserve the pivot across future AI sessions.

## Alternatives and limitations

Inertia is invariant under componentwise rigid alignment; silhouette alone rewards arbitrary separation. The preferred constrained objective balances separation against cross-component ambient-distance stress. This is not proof of novelty: multi-manifold learning and manifold alignment already exist. Graph-connected components need not equal true manifolds. Correctness of local solvers and reliability under unknown generating labels have not been established.

## Evidence and validation boundary

The current GitHub main branch contains the EXP-0001 scaffold and previously verified pip-based CI, not EXP-0002–EXP-0008 source/results. Prior numerical results discussed in chat belong to separate local archives, not a reproducible GitHub revision. No experiment or performance result is claimed by this commit.

No new Python source code was changed, so no numerical test result is asserted for this documentation edit. LaTeX compilation, Ruff, Sphinx and research validation were not executed from an integrated checkout in this session; see the pre-existing CI journal entry for the last verified remote checks.

## Next actions

Perform a source-verified literature novelty matrix, merge/reproduce the local experiments without overwriting existing CI changes, implement an unsupervised radius rule, then compare separation–distortion frontiers against tuned multi-manifold baselines on independent datasets. Only then draft results as a scientific contribution.
