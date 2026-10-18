# PROP-0003 — Exact recovery window for sampled disconnected supports

**Status:** Proved elementary finite-sample observation; **not a novelty claim**.
**Date:** 2026-10-18
**Related:** [TDA and stochastic-geometry program](../research_tda_stochastic_geometry.md)

## Definitions

Let X = X_1 ⊔ ... ⊔ X_K be nonempty finite subsets of Euclidean space, where the groups are the *known underlying generating groups for theorem/evaluation only*. Let G_r(X) be the graph with edge (i,j) exactly when ||x_i-x_j|| ≤ r (r>0). For each k with |X_k| ≥ 2, let

    b_k = max_{edge e in MST(X_k)} length(e).

For |X_k|=1 put b_k=0. Define the maximum internal bottleneck and minimum cross-group separation

    b = max_k b_k,
    δ = min_{k≠l} min_{x in X_k,y in X_l} ||x-y||.

Assume K≥2 and distinct groups so δ>0. The MST is computed on the complete Euclidean weighted graph; its largest edge is the smallest threshold ensuring that group is connected.

## Proposition A: an exact labeling-compatible radius exists iff b < δ

For any r>0, the connected components of G_r(X) are exactly X_1,...,X_K **if and only if** b ≤ r < δ.

**Proof.** The radius-induced subgraph on X_k is connected exactly when r ≥ b_k: a Euclidean MST supplies a connecting spanning tree at and above b_k; conversely, any connected threshold graph has a spanning tree with maximum edge ≤r, contradicting MST's minimum-bottleneck property if r<b_k. There is no cross-group edge exactly when r<δ, using the inclusive edge rule ||x−y||≤r. Thus the full graph has the desired partition exactly under the intersection b≤r<δ. Such an r exists precisely if b<δ. QED.

For small r there may be more than K graph components; for r≥δ there may be fewer (the first cross-group edge merges at least two groups). Existence says nothing about how to select r without generating labels.

Define Γ = δ−b as a *finite-sample recoverability margin*. Positive Γ permits the true partition; negative Γ makes recovery by **one global radius** impossible. The equality case fails because edges at r=δ are included.

## Proposition B: a simple perturbation margin

Suppose there is a pointwise correspondence x_i ↔ x'_i and ||x'_i−x_i||≤ε for every i. Then

    b' ≤ b+2ε,       δ' ≥ δ−2ε.

**Proof.** Each original MST edge increases in length by at most 2ε, and the perturbed MST bottleneck can be no larger than the maximum edge in that perturbed original spanning tree. Every original cross-group distance decreases by at most 2ε, so its minimum does as well. Hence Γ'≥Γ−4ε and Γ>4ε guarantees a nonempty radius interval after perturbation. QED.

This assumes a fixed correspondence and identical group membership; it is not a proof for outliers, missing observations, arbitrary noise distributions, or unknown correspondences.

## Proposition C: H_0 of the Vietoris–Rips filtration

Define VR_r(X) as the clique complex with an edge iff distance≤r. Its 1-skeleton is G_r(X); higher-dimensional simplices do not change connected components. Therefore

    β_0(VR_r(X)) = number of connected components of G_r(X),

and the finite H_0 death times are the n−1 MST merge-edge lengths counted with multiplicity (ties can cause simultaneous deaths).

Thus for b≤r<δ a persistent interval exists where β_0=K with the **true** partition. A plateau at a value K on an arbitrary unknown dataset, however, need not reveal the true K or correspond to unique manifolds; finite samples can produce spurious plateaus.

## Distinct limitations

1. Graph connectivity alone does not ensure graph-shortest-path fidelity: r can bridge *different folds within the same manifold* even while G_r recovers all generating groups.
2. The theorem is conditional on knowing the true partition to define b and δ. An unsupervised estimator of r is a separate unproved problem.
3. Intersecting supports have zero population separation; near contacts, unequal densities, bridges and sampling noise may make Γ nonpositive.
4. This does not guarantee preservation of the full H_0 persistence diagram after embedding. A single x-strip gap is a one-radius condition; compare with TopoMap, which preserves the entire diagram.
5. VR filtration parameter uses **edge distance threshold r**, not union of radius-r balls (Čech nerve connections at 2r in Euclidean space).
