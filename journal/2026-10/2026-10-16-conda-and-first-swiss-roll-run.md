# 2026-10-16 — Conda environment and first Swiss-roll smoke run

**Status:** environment preparation and exploratory computation; no new scientific result is validated.

## Objective and research state

The user requested a Conda-based environment and to begin experiments.
Following the journal-first protocol, the existing EXP-0001 Swiss-roll radius
sweep and the current handoff were reviewed. The root had no `environment.yml`.

## Changes and reasoning

- Added `environment.yml` for Python 3.11 with conda-forge scientific,
  numerical, testing, documentation and baseline dependencies, and editable
  installation of this repository.
- Updated Conda-first setup, the journal, current state, the AI handoff,
  experiment instructions and the structural validator.
- Deferred Docling to a separate optional literature-processing environment.
- Left candidate embedding optimizers unimplemented: EXP-0001 measures the
  radius graph, **not** hybrid Isomap dimensionality reduction.

## Actual local checks

Executed from the earlier starter ZIP snapshot, in a **plain Python** sandbox
(not a Git checkout and **not Conda**):

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python experiments/run_exp_0001.py --config experiments/configs/exp_0001.json --output /tmp/pg_research/exp_0001_initial
```

- 16 tests passed.
- 240 noiseless synthetic Swiss-roll points, fixed seed 20261016.
- Radius, components, edges, within-component geodesic RMSE:
  - 1.5, 88, 231, 1.0524603175
  - 2.5, 16, 618, 2.1398552947
  - 3.5, 3, 1169, 3.0293254760
  - 5.0, 1, 2189, 1.2395593716
  - 7.0, 1, 4431, 26.2789938496

**Limitations:** at different radii the evaluated pair set changes until
connectivity. Large r=7 error is compatible with manifold shortcuts but does
not establish causation. The run had no recorded Git SHA; its output was not
promoted as a paper result. The new Conda environment was **not solved or
tested here** (Conda unavailable). Ruff/Sphinx were also unavailable.

## Rejected alternatives

Avoided labeling preliminary radius-sweep values a controlled comparison.
Avoided pulling the large Docling extraction toolchain into the numerical
Conda environment by default.

## Next actions

Create the Conda environment from a checked-out Git repository, run tests,
Ruff, Sphinx and EXP-0001, capture the commit and `conda list --explicit`,
then implement fair PCA/MDS and Isomap baselines ahead of optimizing hybrid
or componentwise alignment methods.
