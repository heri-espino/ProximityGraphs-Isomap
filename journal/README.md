# Research journal — read this first

**AI start order:** read this file, [`LATEST.md`](LATEST.md), and its linked dated entry **before** reading `AI_HANDOFF.md` or summarized `context/` files. The journal preserves *why* the direction changed; the summaries tell you what is current.

- **Dated, append-only entries:** `YYYY-MM/YYYY-MM-DD-short-topic.md`. If a same-day follow-up occurs, add a distinctly named entry; do not overwrite earlier reasoning.
- **Latest entry pointer:** [`LATEST.md`](LATEST.md), updated after every substantive repository-editing session.
- **Architectural/methodological decisions:** `decisions/ADR-####.md`, with status, options, rationale and consequences. Retired decisions must be marked superseded, not deleted.
- **Current working handoff:** [`../AI_HANDOFF.md`](../AI_HANDOFF.md).
- **Canonical current state and priorities:** [`../context/STATE.md`](../context/STATE.md) and [`../context/NEXT_STEPS.md`](../context/NEXT_STEPS.md).

A dated entry should cover: date, question, inputs/assumptions, actions, changed files, why, evidence including commands/tests/outputs, rejected alternatives, failures, uncertainties, and follow-ups. Link notes, experiments, results and literature by their stable IDs; don't duplicate their full content here.

**Never delete or retroactively rewrite historical findings.** Correct earlier mistakes in a new dated entry, linking the erroneous earlier entry, so a subsequent AI can reconstruct the evolution of the project.
