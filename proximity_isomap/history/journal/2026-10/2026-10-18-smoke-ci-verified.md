# 2026-10-18 — Confirmed rebuilt EXP-001..008 smoke CI

**Evidence:** [GitHub Actions run 39139028489](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39139028489), source commit `95c69a1d48527e59fc07db3648515931e7d15b83`.

## Verified
Python 3.11 and Python 3.12 both passed unit tests, Ruff, the research and numbered archive validators, strict Sphinx, and the new **ContrastColors-pinned experiment smoke test**, which executes all eight rebuilt experiment paths on smaller datasets. Previous CI formatting/link issues were corrected.

## Evidence boundary
Quick smoke outputs were deliberately ignored by Git and were not published as scientific results. **Full EXP-001..008 source recomputation, image publishing and notes updates on the user's Conda/Windows machine remain pending.** Rebuilt methods are not numerically identical to historical unavailable source. No Integration.zip was imported.

## Next
Use `./scripts/run_all.ps1 -Quick` on the target Windows machine; then `./scripts/run_all.ps1 -Push` to generate full PNG/SVG, NPZ/CSV/JSON outputs and automatically embed new figures into numbered notes. Verify the resulting commit and GitHub Actions before using outputs in the paper.
