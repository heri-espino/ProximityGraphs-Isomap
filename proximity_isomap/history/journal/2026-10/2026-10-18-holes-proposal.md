# 2026-10-18 — Proposed H1 hole visualization

**Status:** Conceptual extension and illustrative local simulation; no full EXP-009 benchmark completed.

User suggested detecting and plotting topological holes, in addition to identifying disconnected manifolds.

Scientific distinctions: graph cycles are not necessarily H1 cycles in a filled VR complex; triangular cliques are 2-simplices. True Swiss-roll strips have H1=0; circles and annuli have H1=1; a torus has H1=2 and H2=1. Persistent bars help distinguish stable structures from sampling-induced transient cycles.

An illustrative local 36-point two-circle VR filtration was computed over F2. Two long H1 bars were approximately (0.347296, 1.732051), and a visual preview with two VR scales plus barcodes was generated in the chat container, NOT committed as a canonical ContrastColors output.

Rigid alignment exactly preserves within-component Euclidean distances of independent Z_k, hence all within-component Rips diagrams of Z_k and aligned Y_k. No automatic preservation of original ambient input X_k VR persistence follows. Compare geodesic and ambient VR metrics explicitly.

Next: proposed EXP-009 should include H0/H1 barcode panels, optional H2 for sphere/torus, visually meaningful geometric cycle representatives, original-vs-projected persistence comparison, and negative controls for folds/noise/intersections. Full EXP-001–008 reruns remain pending GitHub issue #6. Preserve the short-paper focus; none of these ideas alone is a novelty claim.
