# 2026-10-18 — Fix EXP-010/011 numbering and require GitHub publication

The user identified that two locally executed experiments were given as ZIP archives without complete GitHub code, original 3D/2D figures and numerical results: EXP-010 (dense cylinder versus five disjoint rings) and EXP-011 (componentwise kNN/radius Isomap versus PCA, global Isomap and t-SNE; genuine UMAP unrun). A professor presentation had also incorrectly occupied experiment 010.

**Correction on GitHub:** Presentation moved to `notes/012-presentation_checkpoint/`; note index updated; EXP-010/011 mathematical notes and numerical-value-derived summary SVG plots committed under their matching numbered folders. Checkpoint 012 now embeds both SVG charts as well as the EXP-001–009 figure atlas.

**Permanent rule:** AGENTS.md and AI_HANDOFF.md now require all future completed experiments to be **published directly to GitHub** with code, original saved results, real PNG/SVG, and mathematical notes, checked by remote commit SHA. No ZIP-only or issue-only handoffs may be presented as completed integration.

**Publication blocker:** The GitHub connector does not transfer original local ZIP binaries into the repository directly. `scripts/import_exp010_exp011.ps1` is committed; user may run it on Windows with the two original ZIPs in Downloads, to import the original runners, complete saved metrics and figures, full illustrated notes, and tests, and push to main after checks. **Full original EXP-010/011 publication remains pending until that push occurs.** The user confirmed they can run both experiments locally. Do not claim the missing original assets are already on GitHub.

This was a documentation/workflow repair; no new numerical experiment was executed. Current Marp export was not visually rendered; native Ruff/Sphinx validations were not run in this connector session.
