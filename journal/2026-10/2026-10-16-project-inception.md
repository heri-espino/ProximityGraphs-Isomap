# 2026-10-16 — Project inception

**Context:** discussion with professor about proximity graphs for Isomap-like dimensionality reduction.

## Ideas considered

1. Use endpoint-distance balls (radius graph) to make adjacency independent of the presence of additional sample points; distinguish from empty-region graphs and ball-intersection rules.
2. Permit disconnected radius graphs instead of automatically adding edges.
3. Investigate pairwise-distance distortion as an objective for embedding all points: graph geodesic distances inside components, ambient Euclidean distances between components.
4. Compare (a) unconstrained hybrid stress optimization and (b) componentwise Isomap followed by rigid alignment of components.

## Cautions

These ideas overlap established methods: Isomap, radius neighborhood graphs, metric MDS, and manifold alignment. The combined approach has **not** been shown novel. On folded manifolds, ambient cross-component distances can be misleading.

## Action taken

Created a research-first repo structure with package, mathematics notes, chronological journal, experiments, results and paper skeleton. Implemented a small baseline—not a complete hybrid optimizer.

## Next

Follow [`../../context/NEXT_STEPS.md`](../../context/NEXT_STEPS.md). No experimental comparison or new theorem claimed.
