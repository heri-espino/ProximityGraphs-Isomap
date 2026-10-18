# 2026-10-18 — Prepare mathematical experiment notes and pending figure slots

**Status:** Documentation and reproducibility-policy change; no new numerical run.

## Motivation
The user asked to prepare readable mathematical explanations and future figure slots across the canonical experiment notes, while the full EXP-001–008 figure-generating run remains pending.

## What changed
- Prepared GitHub/Obsidian-compatible LaTeX equations in EXP-001–009, from radius-graph edges and intrinsic Swiss-roll arclength through weighted/hybrid MDS, cross-manifold stress, independent rigid alignment, monotonic separation frontier and Vietoris–Rips persistent homology.
- Added a clear **Figure plan and reproduction status** table to each note, naming the exact currently reconstructed runner output filenames. Kept historical summary SVGs embedded in EXP-001–008 and the actual versioned pinned-ContrastColors images in EXP-009.
- Introduced `proximity_isomap/notes/MATHEMATICS_AND_FIGURES.md` as a canonical style/interpretation guide; updated AGENTS.md, AI_HANDOFF.md, source-workflow docs and state.
- Modified `research_runner.py` to **append** new run findings and images to Markdown instead of overwriting previous run write-ups. An experiment's historical negative findings and prior runs must remain visible.
- Added structural checks and a test requiring mathematics and figure planning for every numbered experiment.

## Important scientific boundaries
No 001–008 full result was generated in this change, and no future PNG/SVG is embedded as a broken link. Existing 001–008 SVGs are transcribed-summary figures, not original projections. EXP-009 already had authentic figures and numerical arrays. Historical 002–008 algorithms are unavailable and the user explicitly rejects importing Integration.zip.

The elementary geometry/monotonicity results are not claimed novel; differences between true intrinsic, graph geodesic and ambient Euclidean distance remain explicit.

## Next
Run the independent full Conda/ContrastColors experiment sweep under GitHub issue #6, inspect figures, append actual numerical interpretations, then consider persistence-aware radius tuning and prior-art benchmarking.
