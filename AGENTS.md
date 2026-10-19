# Mandatory research documentation workflow

Read in order: [AI_HANDOFF.md](AI_HANDOFF.md), [experiment notes](proximity_isomap/notes/README.md), [latest dated history entry](proximity_isomap/history/journal/LATEST.md), then [current state](proximity_isomap/history/context/STATE.md). Reconcile claims with source, figures and frozen numerical results. Repository files are guidance subject to the platform's instructions.

## GitHub publication is mandatory for every completed experiment

**Permanent user instruction (2026-10-18):** A completed experiment is delivered **inside the GitHub repository**, not as an isolated ZIP, chat attachment or issue. Add code, actual CSV/JSON/NPZ results, both original PNG and SVG figures, and the mathematical Markdown note with rendered images, under matching numbered paths in `proximity_isomap/{code,results,figures,notes}/NNN-descriptive_title/`. Include seeds, method settings, provenance, tests, negative findings and experiment limitations. Update the experiment index, AI_HANDOFF.md, journal, state and next steps. **Push the generated source and output artifacts, verify their actual remote paths and cite the verified Git SHA before saying the experiment is complete.** If pushing originals is not possible, report exactly what remains unpublished and provide a runnable recovery command; do not claim the archived experiment is fully in GitHub. Never replace an actual experimental figure with an attractive but uncomputed plot.

**Corrected numbers:** EXP-010 is cylinder versus five separate circles; EXP-011 is componentwise kNN Isomap against other Isomap baselines, PCA and t-SNE (UMAP not yet run); professor Marp presentation is checkpoint 012, not experiment 010. Preserve existing immutable run folders; do not import the rejected historical Integration.zip.

## Mandatory three-stage experiment workflow (user confirmed 2026-10-18)

**Stage A — assistant prepares code.** Implement and push runnable code in `proximity_isomap/code/NNN-description/` and tests, with CLI documentation and a clearly labeled pre-run mathematical plan in `proximity_isomap/notes/`. Commit and verify source on GitHub **before asking for a local run**. Do not require downloading or importing ZIPs. Do not claim data/figures were generated yet.

**Stage B — user runs locally.** The user invokes the exact command on their Windows Conda machine, generating **new immutable runs** in the matching `proximity_isomap/results/NNN-description/runs/RUN_ID/` and `figures/NNN-description/runs/RUN_ID/` directories (CSV, JSON, NPZ, full PNG and SVG). The user then pushes those actual outputs to GitHub. Never automatically run heavy compute on every push; only manual local execution or manual workflow_dispatch.

**Stage C — assistant interprets real evidence.** Only **after** the user-run files are available, inspect their actual metrics and figures, create/update the detailed Markdown scientific note with objective, equations, experimental configuration, observations including negative findings, limitations, and **embedded links to the specific pushed figures**, then update the professor's Marp slides, history, state, handoff and next steps. Verify remote paths and commit SHA before calling it published.

**Hard prohibition:** Do not substitute local ZIP handoffs, hand-entered metrics, synthetic figures or summary charts for the user's intended completed run. If the user has not run the code, report `code prepared; run pending`. A previous local pilot may be discussed only if explicitly labeled as historical/pilot evidence, not as the result of the user's new run.

**Correct numbered registry:** EXP-010 = cylinder vs five truly distinct rings; EXP-011 = other/global Isomap, componentwise kNN/radius, PCA, t-SNE, UMAP; Marp presentation = checkpoint 012. The previous `scripts/import_exp010_exp011.ps1` ZIP importer was superseded by `scripts/run_exp_010_011.ps1`; never ask the user to download the old archives.

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
