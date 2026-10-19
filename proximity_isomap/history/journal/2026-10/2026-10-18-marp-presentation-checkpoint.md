# 2026-10-18 — Marp presentation checkpoint

## Objective

Prepare a professor-facing mathematics-and-experiments presentation under proximity_isomap/notes/010_presentation_checkpoint/, with source-backed claims and all currently versioned experimental visuals.

## Work and evidence

Created a 63-slide Marp Markdown presentation with 21 versioned experimental PNG panels (EXP-001–009) and 9 separately labeled historical SVG summaries, plus a README for PowerShell PDF/PPTX export. Every referenced GitHub image path was checked against the main-branch recursive tree.

The presentation preserves rigorous distinctions: graph components versus disjoint convex hulls; within-manifold geodesic stress versus cross-manifold ambient stress; exact rigid invariance versus imperfect Isomap geodesic approximation; H0 connectivity versus H1 holes; oracle radius diagnostics versus unsupervised radius selection. The negative EXP-007 between-component distortion finding and EXP-009 H1 losses remain visible.

EXP-010 and EXP-011 experiments were executed locally but their figure archives were not yet committed to GitHub. The deck describes selected provisional numerical findings **without** adding broken image paths. The 001–008 versioned runs are reconstructed implementations, not recovered historical algorithms.

## Files

New Marp presentation and README, notes index, handoff and state/next-steps updates, and this dated journal entry plus latest pointer.

## Validation and boundaries

Checked all figure targets against GitHub API tree. No new experiments, Python tests, local Ruff, Sphinx or Marp browser rendering were executed in this documentation-only connector session. The Marp CLI and math syntax follow official Marp documentation.

## Next

Export PDF/PPTX from a checked-out repository with Marp CLI. Inspect slides visually, and integrate EXP-010/011 versioned figures and full method-comparison results before upgrading these provisional sections.
