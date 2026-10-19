# ProximityGraphs-Isomap

Research on separation-constrained Isomap for disconnected manifolds. **Novelty and comparative superiority have not been established.**

The canonical experiment records are [proximity_isomap/notes/](proximity_isomap/notes/README.md), with matching numbered folders under [code](proximity_isomap/code/README.md), [figures](proximity_isomap/figures/README.md), and [results](proximity_isomap/results/README.md). Old journals, original experiments and context are preserved under [history](proximity_isomap/history/README.md), not deleted. [Mathematical results](proximity_isomap/notes/mathematics/index.md) and [the short working paper](paper/RESEARCH_DIRECTION.md) are separate.

## Windows PowerShell

Install Git and [Miniforge](https://github.com/conda-forge/miniforge), open a Conda-ready PowerShell window, then:

~~~powershell
git clone https://github.com/heri-espino/ProximityGraphs-Isomap.git
cd ProximityGraphs-Isomap
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run_all.ps1 -Quick
.\scripts\run_all.ps1 -Push
~~~

The script creates/updates the environment from `environment.yml`, including [contrastcolors](https://github.com/heri-espino/Colors) pinned to commit `84e05b4`, runs tests and all **newly reconstructed** EXP-001..008 experiments, saves CSV/JSON/NPZ and genuine PNG/SVG figures, and embeds the PNGs into each note. `-Quick` is a local smoke test; `-Push` runs the full suite, commits and pushes. Without `-Push`, no changes are uploaded.

**Methodological qualification:** this rebuild does NOT import the unavailable historical Integration.zip. Algorithms and numeric results may differ from those older runs. Synthetic generating labels are still used for some diagnostic radii. The reusable library stays in `src/proximity_isomap/`, literature in `literature/`, tests in `tests/`, manuscript in `paper/`.

Read [AGENTS.md](AGENTS.md) and [AI_HANDOFF.md](AI_HANDOFF.md) before extending the experiments.


## EXP-010 / EXP-011 — local computation, GitHub publication, then scientific analysis

[EXP-010 — cylinder versus five rings](proximity_isomap/notes/010-radius_density_and_rings/README.md) · [EXP-011 — Isomap/kNN and PCA/t-SNE/UMAP comparisons](proximity_isomap/notes/011-isomap_baselines/README.md) · [Checkpoint 012 — Marp presentation](proximity_isomap/notes/012-presentation_checkpoint/README.md).

**Working rule:** assistant pushes the runnable code and pre-run mathematical plan; user runs it on the Windows Conda machine and pushes actual numeric CSV/NPZ/JSON and PNG/SVG; assistant then reads the run files and writes the detailed experimental Markdown interpretation with real embedded figures, updating the Marp checkpoint. Do not use ZIP import and do not interpret a run that has not happened.

~~~powershell
git pull --ff-only
conda install -n proximity-isomap -c conda-forge umap-learn -y
.\scripts\run_exp_010_011.ps1 -Quick
.\scripts\run_exp_010_011.ps1 -RequireUmap
~~~

The quick run is disposable/ignored. Full runs receive unique labels and never overwrite earlier runs. **Nothing is automatically pushed.** Inspect the generated outputs, commit and push only their full-run folders under `proximity_isomap/results/` and `proximity_isomap/figures/`. No Ruff or old `scripts/run_all.ps1` invocation is required for EXP-010/011.

Note that the previously committed 010/011 numerical **summary SVGs** describe an *older exploratory pilot*, not the upcoming fresh run. The assistant will update both experiment notes after inspecting the user's exact new files.


## Mathematical lecture (checkpoint 012)

[Componentwise kNN-Isomap — Marp Markdown lecture](proximity_isomap/notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md) derives kNN graphs, graph geodesics, MDS, rigid alignment, geometric clearance, evaluation metrics, complexity and limitations, using the executed full EXP-010/011 run figures. [Marp rendering instructions](proximity_isomap/notes/012-presentation_checkpoint/README.md).


## EXP-013 — Classical multicomponent dashboards (code ready, run pending)

[Mathematical experiment protocol](proximity_isomap/notes/013-classical_multicomponent_dashboards/README.md) · [Native Python implementation](proximity_isomap/code/013-classical_multicomponent_dashboards/run.py) · [PowerShell launcher](scripts/run_exp_013.ps1).

Seven classical manifold families in far/near regimes generate **28 real 3×3 dashboards** (one Isomap-centered and one general dimensionality-reduction comparison per scenario), plus 3D source views and k-sensitivity diagnostics. User must execute and push actual images/metrics. Only then will the assistant write run-specific results and incorporate all dashboards into the shared research lecture.
