# PROP-0002 — Rigid component invariance and the separation frontier

**Status:** Proven elementary properties under the assumptions below. They are not claims of mathematical novelty.
**Date:** 2026-10-17
**Context:** [Working paper thesis](../../paper/RESEARCH_DIRECTION.md)

Let Z_1,...,Z_K be finite point sets in R^d, each with rows z_i. For Q_k in O(d) and translations t_k, define Y_k = {z_i Q_k + t_k : z_i in Z_k}. Let s > 0 and mu > 0.

## Claim A: Within-component distance invariance

For i,j in the same component k,

    ||(z_i Q_k+t_k) - (z_j Q_k+t_k)||_2^2
      = (z_i-z_j) Q_k Q_k^T (z_i-z_j)^T
      = ||z_i-z_j||_2^2.

Thus the alignment leaves **distances in the independently embedded Z_k** unchanged. It does not prove that Z_k preserves true intrinsic manifold distances.

## Claim B: Ordered strips suffice for convex-hull clearance

Choose a unit direction u (e.g. the horizontal axis). Suppose the components have been ordered and

    min_{y in Y_{k+1}} <u,y> - max_{y in Y_k} <u,y> >= mu*s

for every k=1,...,K-1. Since a linear functional takes its extrema on the vertices of a finite convex hull, the same inequalities hold for every point in conv(Y_k) and conv(Y_{k+1}). Summing neighboring gaps establishes separation >= mu*s in the u-projections of any two distinct component hulls. By Cauchy–Schwarz, Euclidean distance between any two hull points is at least their projected gap >= mu*s. Hence all hulls are disjoint and have Euclidean clearance at least mu*s.

The converse fails: two disjoint convex hulls can be separable in directions that are incompatible with one fixed global ordering/axis. The strip constraint is sufficient, not necessary, for hull separation.

## Claim C: Nondecreasing ideal separation–distortion frontier

Let F(mu) denote the feasible alignments satisfying convex-hull clearance at least mu*s, and let E_cross be any fixed, well-defined placement objective. Define V(mu) = inf_{Y in F(mu)} E_cross(Y), with inf(empty) = +infinity. If mu_2 >= mu_1, then F(mu_2) is a subset of F(mu_1), so V(mu_2) >= V(mu_1).

This is a set-inclusion argument, not a convexity claim. A nonconvex solver's local minima, especially with changing initialization or approximate anchor objectives, need not respect empirical monotonicity.

## Boundary cases

For K=1, the clearance and cross-component objectives are not applicable. For singleton components, no within-component pair distance is available, so any normalization based on within-component distances requires a positive alternative scale or must be declared undefined. These proofs do not address the nonconvex optimizer's global convergence.
