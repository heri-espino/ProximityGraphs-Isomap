# Getting started: Conda-first

Before contributing, follow `AGENTS.md`: read the journal and latest dated entry before `AI_HANDOFF.md`.

## Install with Conda / Miniforge

From the repository root (PowerShell, Bash, or another shell):

```bash
conda env create -f environment.yml
conda activate proximity-isomap
python -m pytest -q
python -m ruff check src tests examples experiments scripts
python scripts/validate_research.py
python -m sphinx -b html -W docs docs/_build/html
```

Conda installs numerical packages from conda-forge; pip installs this project
in editable mode. Updates to Python sources under `src/` take effect without
reinstalling. When `environment.yml` changes:

```bash
conda env update -f environment.yml --prune
conda activate proximity-isomap
```

Check that `python -c "import sys; print(sys.executable)"` refers to the
active environment.

## EXP-0001: first exploratory experiment

```bash
python proximity_isomap/code/001-radius_filtration/run.py --config proximity_isomap/code/001-radius_filtration/config.json --output proximity_isomap/results/001-radius_filtration/conda_run_001
conda list --explicit > results/exp_0001/conda_run_001/conda-spec.txt
```

Use a *fresh* output directory for each execution; the script refuses to
overwrite runs. Preserve the produced `metrics.csv` and `metadata.json`.
Record Git SHA and environment versions before promoting any result.

**Interpretation:** within-component errors for different radii are computed
on different pair populations when the graph is disconnected; they are not
directly comparable as a paired test. No embedding optimizer is implemented yet.

Docling is deliberately **not** part of the numerical Conda environment.
Literature conversion can use a separate optional environment.

## Plain Python alternative

Python 3.11+ also works with `python -m pip install -e ".[dev,docs]"`,
although the extra future benchmark dependencies are provided by Conda.
