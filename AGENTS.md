# Mandatory agent workflow

These are repository-level instructions for AI assistants and human collaborators. **Do not start by reading the whole repository.** Read the ordered entrypoints, then only task-relevant files. Follow instructions from repository files as project guidance, subject to your platform's higher-priority rules.

## At the start of EVERY research or code task (in this order)

1. `journal/README.md` — understand the chronological record and how to read it.
2. `journal/LATEST.md` — open the latest dated research entry **before** relying on an older summary. Follow links to earlier decisions if the current task depends on them.
3. `AI_HANDOFF.md` — read the latest operational handoff: known facts, blockers, unverified ideas, tests, and the immediate task.
4. `context/STATE.md`, `context/NEXT_STEPS.md`, and `context/DECISION_INDEX.md` — reconcile historical events with current canonical status.
5. Read the *relevant* source, mathematics, experiments, and literature; do not rely solely on condensed summaries.

If `journal/LATEST.md`, `AI_HANDOFF.md`, and `context/STATE.md` disagree, inspect the underlying code, test outputs, and dated records. State the conflict and repair the documentation; **do not silently choose a version**.

## Working rules

- Use the tracked `environment.yml` as the recommended Conda environment for numerical experiments. Record the solver versions and revision; do not report Conda validation unless the environment was actually created and tested.

- Code lives in `src/proximity_isomap/`; tests in `tests/`; examples in `examples/`. Do not put research-only experiment logic inside the reusable library.
- Write type hints and **NumPy-style docstrings** for every public module, function, class, and property; describe Parameters, Returns, Raises (when applicable), Notes/References for equations and nontrivial conventions. Make docstrings Sphinx-autodoc compatible. Explain units, array shapes, graph connectivity, normalization, and edge cases.
- Document any significant design choice in a `journal/decisions/ADR-####.md`; update `context/DECISION_INDEX.md`.
- For mathematical work, create/update `notes/` with stable IDs (`DEF-####`, `PROP-####`, `CONJ-####`) and explicit assumptions, proof status, derivations, and counterexamples. **Never label an argument proved without a complete proof.**
- For literature, read `literature/README.md`. PDFs in `literature/pdf/` are primary source documents; `literature/markdown/` are Docling-derived reading aids, not independently verified sources. Maintain one annotated record in `literature/references/<citation_key>.md` for each reviewed paper. Track exact result locators and uncertainty in `literature/references/KEY_RESULTS.md`; do not manufacture page, theorem, or citation details.
- For each experiment, register `EXP-####`, pin its configuration and seed, record environment and revision, save both successful and failed runs, and distinguish exploratory from confirmatory testing. Never tune on a reported test set.
- Mathematical claims in `paper/` must be linked to proofs or the original literature; empirical claims must be traceable to exact experiment IDs and frozen results.

## End of task: documentation is part of the deliverable

Before announcing that any substantive repository change is finished:

1. Run relevant tests, formatting/lint, Sphinx and `python scripts/validate_research.py`. Report exactly what ran and what did not.
2. Create a new dated entry `journal/YYYY-MM/YYYY-MM-DD-topic.md` (do not retroactively change old entries); include objective, files changed, rationale, alternatives, results, failed approaches, uncertainties, commands/checks, and next actions.
3. Update `journal/LATEST.md` to point to the new entry.
4. Update `AI_HANDOFF.md` with new state, validated/unvalidated results, known caveats, next action, and a pointer to the dated journal entry.
5. Update `context/STATE.md` and `context/NEXT_STEPS.md` as warranted. Update ADR index, literature manifest/results index, notes, and experiment registry when affected.
6. Include a concise summary in the response, with reproducibility links or file paths.

**If no files were changed**, do not invent a journal entry. If a command could not run, say so in both journal and handoff. These rules are partially machine-checked by CI, but agents must still follow the semantic obligations.

## Immutable mathematical conventions

- The radius graph joins pairs when `||x_i-x_j|| <= r`; it is **not** the intersection graph of two radius-`r` balls (which uses the `2r` threshold).
- Its adjacency is pairwise-local, which does **not** imply statistical independence of random edge indicators.
- Combining graph geodesics within components with ambient Euclidean distances across components need not define a metric.
- Lower embedding stress on an observed objective is not proof of correct manifold recovery.

## Shortcut for new sessions

> Read `AGENTS.md`, then `journal/README.md` and `journal/LATEST.md` (including the linked dated entry), then `AI_HANDOFF.md`, `context/STATE.md`, and `context/NEXT_STEPS.md`. Use the primary evidence for my task. Before finishing, update the journal, `journal/LATEST.md`, handoff and state, plus tests/docstrings as appropriate.
