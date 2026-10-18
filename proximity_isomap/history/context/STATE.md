# Current state (2026-10-18)

The repository has a single numbered `proximity_isomap/` research archive, historic dated journal and decisions under `history/journal/`, and proofs under `notes/mathematics/`. The root journal/context/legacy experiments/results/figures/notes were moved; old content preserved in history.

Eight new executable experiment implementations are included in `proximity_isomap/code/research_runner.py` and numbered wrappers. They are reconstructions, **not identical historical algorithms**. The user explicitly does not want Integration.zip imported.

All figures will use `contrastcolors` pinned from `heri-espino/Colors`, white publication style and Okabe–Ito palette. Running the Windows PowerShell script produces new actual figures and saves them in numbered folders, and embeds PNGs in the corresponding README notes.

**Not yet executed by user:** full Conda-based experiments and their generated outputs. CI can confirm code quality but not the unrun science. Paper remains a prospective separation–distortion methods contribution, not proved novel.

## Verification (2026-10-18)

[GitHub Actions run 39139028489](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39139028489) succeeded for Python 3.11/3.12: tests, lint, research validators, Sphinx and Quick-mode runs of all eight newly reconstructed experiments with the pinned ContrastColors library. Full Conda runs are still pending user execution; source and historical numeric parity cannot be inferred from smoke results.
