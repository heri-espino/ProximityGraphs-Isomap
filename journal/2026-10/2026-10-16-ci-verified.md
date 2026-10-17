# 2026-10-16 — GitHub CI verified

**Status:** successful software/documentation verification; no new scientific claim.

## Evidence

GitHub Actions run [38997728144](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/38997728144) for commit
`e7cc9bcf723e72ebec7ec0d133f03d117020b56d` completed successfully on
**Python 3.11 and Python 3.12**. In both jobs:

- Editable pip package installation succeeded.
- All 16 unit tests passed.
- Ruff lint passed.
- The research/literature integrity validator passed.
- Sphinx HTML documentation built with `-W` (warnings as errors).

The previous Ruff failure was addressed by a minimal follow-up patch;
see the preceding journal entry for the four lint diagnostics.

## Important boundary

The CI workflow uses Python/pip, **not the Conda environment**.
The tracked `environment.yml` has not been solved or tested here. EXP-0001's
initial smoke results remain exploratory and lack a versioned Conda run;
they must not be represented as evidence of hybrid Isomap improvements.

## Files updated

Journal latest pointer, this new journal record, AI handoff, context state,
and next steps. No numerical source code or experiment config was changed.

## Next

Create/activate `proximity-isomap` through Conda on a Conda-enabled
machine; run EXP-0001 from the Git checkout, save metrics, Git SHA, and
an explicit package manifest. Then implement and compare standard
Euclidean MDS/PCA and connected Isomap baselines fairly.
