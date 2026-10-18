# Experiment notes: EXP-001–EXP-008

**Read these summaries when you want to know what we tried, what happened, and what it means.** `journal/` instead records when and why decisions changed. Each note links its code, results and figure directory.

| ID | Research question | Main finding | Notes |
|---|---|---|---|
| 001 | Radius graphs and first geodesic diagnostics | Implemented on GitHub (EXP-0001); smoke metrics present | [Open](./001-radius_filtration/README.md) |
| 002 | Hybrid MDS and comparison baselines | Historical local ZIP; source/figures/raw outputs not present on main | [Open](./002-hybrid_mds/README.md) |
| 003 | Small-to-large radius grid | Historical local ZIP; original raw output not present on main | [Open](./003-wide_radius_grid/README.md) |
| 004 | Radius transfer across sampling density and geometry | Historical local ZIP; aggregate numbers transcribed | [Open](./004-radius_transfer/README.md) |
| 005 | Two Swiss rolls and two S-curves | Historical local ZIP; aggregate numbers transcribed | [Open](./005-paired_manifolds/README.md) |
| 006 | Rotated Swiss-roll pair: harder PCA baseline | Historical local ZIP; four-seed aggregate numbers transcribed | [Open](./006-rotated_swiss_rolls/README.md) |
| 007 | Two-component rigid alignment and non-overlap | Historical local ZIP; four-seed aggregate numbers transcribed | [Open](./007-component_alignment/README.md) |
| 008 | One through six independently embedded Swiss rolls | Historical local ZIP; one-seed summary transcribed | [Open](./008-multiple_swiss_rolls/README.md) |

## Conventions

1. Preserve the experiment ID and numbered slug permanently. **007 = two-component alignment; 008 = one-to-six Swiss rolls**.
2. Record *question, hypothesis, configuration, attempted variants, numerical evidence, negative results, interpretation, limitations, next action*. Cite figures by relative Markdown links only if the file actually exists.
3. `summary.svg` is a newly reconstructed plot from rounded archived summary numbers, **not** a recovered original 3D/2D projection. No fake screenshots.
4. Distinguish **within-manifold intrinsic geodesic stress** from **between-manifold original ambient Euclidean stress**; disconnected manifolds have no finite true cross-manifold geodesics.
5. Figures and result files must have matching IDs and provenance; not all historical resources are presently available.
