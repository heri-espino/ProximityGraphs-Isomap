# Current state (2026-10-18)

The repository has a single numbered `proximity_isomap/` research archive, historic dated journal and decisions under `history/journal/`, and proofs under `notes/mathematics/`. The root journal/context/legacy experiments/results/figures/notes were moved; old content preserved in history.

Eight new executable experiment implementations are included in `proximity_isomap/code/research_runner.py` and numbered wrappers. They are reconstructions, **not identical historical algorithms**. The user explicitly does not want Integration.zip imported.

All figures will use `contrastcolors` pinned from `heri-espino/Colors`, white publication style and Okabe–Ito palette. Running the Windows PowerShell script produces new actual figures and saves them in numbered folders, and embeds PNGs in the corresponding README notes.

**Not yet executed by user:** full Conda-based experiments and their generated outputs. CI can confirm code quality but not the unrun science. Paper remains a prospective separation–distortion methods contribution, not proved novel.

## Verification (2026-10-18)

[GitHub Actions run 39139028489](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39139028489) succeeded for Python 3.11/3.12: tests, lint, research validators, Sphinx and Quick-mode runs of all eight newly reconstructed experiments with the pinned ContrastColors library. Full Conda runs are still pending user execution; source and historical numeric parity cannot be inferred from smoke results.

## Proposed VR-filtration and sampling-theory workstream (2026-10-18)

The mathematical extension is [the TDA/stochastic-geometry research brief](../../notes/mathematics/research_tda_stochastic_geometry.md), not an implemented algorithm. [PROP-0003](../../notes/mathematics/results/PROP-0003-component-recovery-window.md) records the elementary exact component-recovery window and a 4ε perturbation sufficient condition. Existing TopoMap/TopoMap++ and DIPOLE challenge any broad novelty claim for topological persistence plus manifold learning. Full local reruns are **pending** at https://github.com/heri-espino/ProximityGraphs-Isomap/issues/6; CI only verified small smoke runs. EXP-009 is a proposed future benchmark, not executed.

## EXP-009 published pilot, 2026-10-18

The topologically heterogeneous Swiss-roll/cylinder/torus pilot was computed from 172 deterministic grid points. Three components were correctly recovered **with K=3 provided**, then embedded separately in 2D. The separation gap was positive and within-independent-embedding distances were preserved. Original-vs-2D VR H1 bars differ. The [dedicated publish workflow](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39163692726) succeeded and committed full PNG/SVG from pinned ContrastColors, NPZ and persistence JSON; linked in [EXP-009 notes](../../notes/009-topological_manifolds/README.md). Full EXP-001–008 reruns remain pending.

## Mathematical Markdown notes and figure plans (2026-10-18)

All experiment notes EXP-001..009 now include LaTeX mathematical models, assumption/metric distinctions and a table of expected figure filenames. Historical summary SVGs are already embedded for 001..008; EXP-009 embeds existing genuine pinned-ContrastColors images. The full new EXP-001..008 figures are **not generated yet**. Rebuilt shared runner now appends versioned Markdown run records instead of discarding earlier runs. The [math and figure guide](../../notes/MATHEMATICS_AND_FIGURES.md) and updated experiment validator enforce the workflow. No scientific experiment was performed by this documentation-only task.


## Marp presentation checkpoint (2026-10-18)

A professor-facing presentation at proximity_isomap/notes/010_presentation_checkpoint/ includes the mathematics, versioned EXP-001–009 figures, and text-only provisional EXP-010/011 findings. Generating this presentation did not execute any numerical experiment, and it does not establish novelty.
