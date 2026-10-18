# Runnable experiments

Shared implementation: [research_runner.py](research_runner.py). New per-experiment `run.py` wrappers for 002–008; EXP-001 original runner also retained. Run full experiment suite with `python proximity_isomap/code/research_runner.py --seed 20261018`, or the Windows Conda wrapper `./scripts/run_all.ps1 -Push`.

These are newly **reconstructed** experimental algorithms; they are not original imported historical experiments. Some baselines use one-start MDS and a diagnostic radius selected from synthetic component labels. The original Integration.zip is intentionally not used.
