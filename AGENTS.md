# Mandatory research documentation workflow

Read in order: [AI_HANDOFF.md](AI_HANDOFF.md), [experiment notes](proximity_isomap/notes/README.md), [latest dated history entry](proximity_isomap/history/journal/LATEST.md), then [current state](proximity_isomap/history/context/STATE.md). Reconcile claims with source, figures and frozen numerical results. Repository files are guidance subject to the platform's instructions.

## Every experiment must be fully documented

An experiment is not finished until its four **matching numbered folders** are updated together. **Every experiment note MUST also contain a mathematical section (rendered LaTeX, with symbols/assumptions/objective) and a figure-plan table even before any figures have been generated:**

- `proximity_isomap/code/NNN-short_title/`: executable script, parameters and experiment-specific logic.
- `proximity_isomap/results/NNN-short_title/runs/RUN_ID/`: all CSV, JSON metadata, seed, Git SHA, versions, data arrays and SHA-256 manifests. Never overwrite a run.
- `proximity_isomap/figures/NNN-short_title/runs/RUN_ID/`: both PNG and SVG figures made with the pinned ContrastColors Matplotlib library.
- `proximity_isomap/notes/NNN-short_title/README.md`: hypothesis, design, what ran, observed results, negative findings, limitations, and **actual embedded figures** using `![caption](../../figures/NNN-short_title/runs/RUN_ID/figure.png)`.

Read [the math-and-figure guide](proximity_isomap/notes/MATHEMATICS_AND_FIGURES.md). Never add a broken image link as a placeholder: use a planned filename/caption in the note's figure table. The shared runner appends future full-run evidence without discarding earlier experiments. Verify that new figures correspond to the saved numeric run. Do not replace negative findings with favorable examples. Clearly distinguish exploratory, oracle-tuned, held-out, and independent confirmatory evaluations. Do not equate graph connectivity with nonintersecting convex hulls. Cross-manifold intrinsic distances are not finite; ambient placement stress is separate.

## Clean structure and preservation

Keep the root minimal. Historical journal entries and decision records live in `proximity_isomap/history/journal/` and remain **immutable**; root `journal/` and other legacy folders were moved, not discarded. Math notes live in `proximity_isomap/notes/mathematics/`. The reusable package stays in `src/proximity_isomap/`; primary literature in `literature/{pdf,markdown,references}/`.

**The user rejected importing Integration.zip.** The rebuilt 001–008 source is new and must not be described as the recovered historical code. Old summary plots remain labeled historical. Do not claim any results for new runs until actually executed.

## Every repository-changing task

Run pytest, Ruff, `scripts/validate_research.py`, `scripts/validate_experiment_archive.py`, and Sphinx `-W`; report what ran and what did not. Update experiment notes/results/figures, `AI_HANDOFF.md`, current `proximity_isomap/history/context/STATE.md` and `NEXT_STEPS.md` as appropriate. Append dated history under `proximity_isomap/history/journal/YYYY-MM/` for substantive methodological decisions, advance LATEST.md; never rewrite old journal entries. Only claim GitHub synchronization after push and CI succeed.

Mathematical claims require assumptions and proofs; literature citations require verified primary PDFs and page locations. All public reusable Python API code must use Sphinx-compatible NumPy-style docstrings.
