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


## Corrected numbering and archive publication

[EXP-010: cylinder versus five separate rings](proximity_isomap/notes/010-radius_density_and_rings/README.md) · [EXP-011: componentwise kNN Isomap and baselines](proximity_isomap/notes/011-isomap_baselines/README.md) · [012: professor Marp presentation](proximity_isomap/notes/012-presentation_checkpoint/README.md). The EXP-010/011 **runnable source is now on GitHub**. Run it on the local Windows/Conda machine using `scripts/run_exp_010_011.ps1 -RequireUmap`, push new immutable CSV/NPZ/JSON and PNG/SVG outputs, then request a data-grounded Markdown interpretation. GitHub summaries are already present, but archives alone are not complete published experiments. See AGENTS.md.
