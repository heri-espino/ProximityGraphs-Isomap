# Presentation checkpoint 012 — professor meeting and mathematical lecture

Two **Marp Markdown presentations** are now in this folder:

- [Research checkpoint](presentation.md) — the existing research chronology, expanded mathematical explanations and all EXP-001–011 versioned figures, including the completed 2026-10-19 full-run EXP-010/011 PNG galleries and actual UMAP results.
- [Componentwise kNN-Isomap: a mathematical lecture](componentwise_knn_isomap_lecture.md) — **53 lecture slides**, deriving kNN graph construction and connectivity, graph geodesics, classical MDS double centering, positive eigendecomposition, rigid-motion invariance, convex-hull separation, centroid-distance objectives, frontier monotonicity, complexity, topological limitations and the EXP-013 experiment design.

Both decks use actual figures from the committed run 20261019T061001Z-full. EXP-010/011 results have been interpreted in their [EXP-010 notes](../010-radius_density_and_rings/README.md) and [EXP-011 notes](../011-isomap_baselines/README.md). **EXP-013 is only proposed**, not executed or claimed as new data.

## Render from the repository root (PowerShell)

Node.js and a supported installed browser are needed for PDF/PPTX conversion; no rerun of a numerical experiment is necessary.

~~~powershell
npx --yes @marp-team/marp-cli@latest proximity_isomap/notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md --allow-local-files --pdf -o componentwise_knn_isomap_lecture.pdf
npx --yes @marp-team/marp-cli@latest proximity_isomap/notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md --allow-local-files --pptx -o componentwise_knn_isomap_lecture.pptx

npx --yes @marp-team/marp-cli@latest proximity_isomap/notes/012-presentation_checkpoint/presentation.md --allow-local-files --pdf -o presentation_checkpoint.pdf
~~~

The Markdown image paths are verified on GitHub. The rendered slides have **not yet been visually inspected** in PDF/PPTX, so review equation sizes and table overflow before presenting.

## Mathematical and evidence boundaries

- The current EXP-011 **componentwise kNN Isomap** implementation uses radius or supplied-K MST detection **followed by** a symmetrized **10-NN graph inside each component**; it is not yet an entirely kNN-based unsupervised partitioner.
- Classical MDS minimizes centered Gram-matrix strain rather than exactly minimizing raw geodesic-distance stress.
- Rigid placement preserves computed within-embedding pair distances but can change original ambient cross-component distances.
- The centroid loss does not identify component orientations when local embeddings are centered.
- Convex-hull clearance and the ideal separation–distortion frontier are explicitly proposed optimization ingredients; EXP-011 uses a feasible strip layout, not the global constrained optimum.
- One full synthetic-seed comparison is evidence, not a claim of universal superiority or established novelty.
