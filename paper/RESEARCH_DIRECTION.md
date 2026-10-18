# Research direction: Component-aware Isomap with a separation–distortion tradeoff

**Status:** Working thesis, October 17, 2026. This is a research proposal, not a novelty or performance claim.
**Intended format:** Concise methods paper inspired by the clarity of the original Isomap paper (about 5–7 pages of main text, subject to journal requirements).
**Working title:** *Separation-Constrained Isomap for Disconnected Manifolds*.

## The central question

**How much global geometric fidelity must we sacrifice to keep independently unfolded manifolds geometrically separate in a common low-dimensional embedding?**

The potential contribution is not an algorithm that separates six Swiss rolls. It is an explicit framework for controlling and measuring the tradeoff between (i) intrinsic geometry preservation, (ii) separation of disconnected components, and (iii) fidelity of their relative placement.

## Candidate contributions — all require novelty verification

1. **Unsupervised graph partition:** build a neighborhood/proximity graph from observations only; use its connected components as candidate manifolds, without oracle generating labels.
2. **Independent intrinsic embedding:** estimate finite graph geodesics *within* each component and embed each separately (e.g. classical MDS/Isomap). This preserves the geometry of each independently computed embedding under later rigid alignment, not necessarily the unknown true manifold distances.
3. **Guaranteed geometric separation:** rigidly align component embeddings subject to positive geometric clearance, rather than relying on disconnected graph labels or favorable initialization to prevent overlap.
4. **A separation–distortion framework:** vary the required normalized clearance and measure the best achievable intercomponent placement fidelity at fixed intracomponent geometry. Study the optimal frontier and scalability beyond two components.

These are **candidate differentiators as a combination**. Radius graphs, multi-manifold methods, separate embedding, alignment, silhouette scores and simple distance-invariance observations already have substantial precedent. No novelty claim should be made without a documented prior-art comparison.

## Problem and notation

Let observations be X = {x_1,...,x_n} in R^D. For radius r > 0, construct an undirected graph with edge (i,j) if and only if ||x_i-x_j||_2 <= r, weighted by Euclidean length. Let C_1,...,C_K denote its connected components. The *graph* component labels need not equal the unknown generating manifold labels.

For each component, obtain a d-dimensional Isomap representation Z_k from finite within-component shortest-path dissimilarities. Write its points as row vectors z_i in R^d. Rigid alignment produces

    y_i = z_i Q_k + t_k, for i in C_k,
    Q_k in O(d), t_k in R^d, Q_k^T Q_k = I.

A rigid transformation preserves all pairwise Euclidean distances **within Z_k** exactly. How accurately Z_k represents true intrinsic distances is a separate empirical issue.

For K >= 2, define the *relative placement stress*

    E_cross(Y) = sqrt[
       sum_{k<l} sum_{i in C_k,j in C_l}
         (||y_i-y_j||_2 - ||x_i-x_j||_2)^2
       /
       sum_{k<l} sum_{i in C_k,j in C_l}
         ||x_i-x_j||_2^2
    ].

Assume the denominator is positive. This uses *ambient Euclidean distances* across distinct components; intrinsic geodesics between disconnected manifolds are not finite.

Define geometric clearance by the distance between convex hulls:

    M(Y) = min_{k<l} dist(conv(Y_k), conv(Y_l)).

For a positive reference scale s (specified before fitting, e.g. a median nonzero within-component target distance), define normalized clearance M(Y)/s. Strictly positive clearance ensures non-intersecting convex hulls, which is stronger than merely distinct graph labels. For K=1, E_cross and M are **not applicable** and should not be assigned artificial values.

## Primary optimization

For a dimensionless separation requirement mu > 0, consider

    V(mu) = inf_{Q_k in O(d), t_k in R^d}
                E_cross(Y)
            subject to M(Y) >= mu*s
                       and Y_k = Z_k Q_k + t_k.

An implementation may impose ordered, disjoint coordinate strips as a *stronger, computationally convenient sufficient condition* for hull separation. That restriction can exclude feasible arrangements and worsen placement stress; the chosen ordering and axis must be reported.

We may later investigate a more flexible formulation that permits small changes inside each component:

    minimize E_cross(Y)
    subject to E_within(Y) <= epsilon
               M(Y) >= mu*s,

with E_within defined against componentwise graph-geodesic targets. This is **not** the same problem as rigid alignment and should be treated as a distinct variant.

## Simple mathematical properties — not claims of novelty

- **Rigid invariance:** ||(z_i-z_j)Q_k||_2 = ||z_i-z_j||_2 when Q_k is orthogonal.
- **Separation by ordered strips:** if max_{i in C_k}(y_i)_1 + mu*s <= min_{j in C_{k+1}}(y_j)_1 for each adjacent ordered pair, then all component convex hulls are disjoint with positive pairwise clearance.
- **Ideal frontier monotonicity:** if mu_2 >= mu_1, the feasible set for mu_2 is a subset of that for mu_1. Thus V(mu_2) >= V(mu_1) when inf(empty set) = +infinity. Numerical *local* optimizers are not guaranteed to produce monotone measured curves.

Full elementary arguments and assumptions are in [PROP-0002](../proximity_isomap/notes/mathematics/results/PROP-0002-rigid-separation-frontier.md). These statements help make the method auditable; they are not yet a nontrivial theoretical contribution.

## Evaluation: three separate axes

1. **Intrinsic fidelity (lower better):** normalized stress between projected within-*true*-manifold distances and analytically known intrinsic geodesics, where synthetic ground truth exists. On real data, report graph-target stress as a surrogate, clearly labeled.
2. **Separation (higher better / hard constraint):** minimum normalized convex-hull gap, count of intersecting component hulls, and comparison with silhouette as a descriptive secondary metric. Increasing silhouette alone is not adequate because arbitrary translation can inflate it.
3. **Global placement (lower better):** E_cross, using ambient original distances across distinct components; report the cost of increasing required gap.

Also report component count, incorrect merges/splits when generating labels are available *for evaluation only*, runtime, solver convergence, and sensitivity to radius and initializations. Distinguish full pairwise stress evaluation from representative-anchor approximations used to *fit* alignment.

## Minimum decisive evidence

- **Figure 1:** One controlled multi-manifold example: 3D originals, PCA, standard/tuned Isomap with an explicit disconnected-graph policy, free componentwise embedding and constrained alignment (same samples and colors).
- **Figure 2:** The empirical separation–placement-distortion frontier for several mu values, with within-component stress as a check; show uncertainty over independent datasets and an existing multi-manifold baseline.
- **Main table:** tuned comparable baselines, paired evaluation, runtime, overlap incidence, and both stresses.

Use rotated multi-roll settings (K=1,...,6), varying orientation, density, gap, and noise. The earlier EXP-0002–EXP-0008 work was produced in local ZIP archives and is **not incorporated or independently reproduced on GitHub main as of this update**. Do not cite its numerical findings in the manuscript until code, frozen results, environment, commit and audits are integrated.

## What would count as success or a negative result?

A defensible contribution must show at least one substantive advantage or mathematically new property beyond prior multi-manifold and alignment methods, while documenting unavoidable tradeoffs. If the only advantage is prettier non-overlapping plots and the placement stress is worse than competitive baselines, the paper's claims must be narrowed or the method reconsidered. If an existing method already solves essentially the same constrained problem, do not claim novelty.

## Prior-art checklist (not yet source-verified)

Study the original Isomap paper, multi-manifold Isomap and stitching methods, discriminant Isomap, joint/weighted MDS, constrained manifold alignment, and cluster separation metrics. Register PDFs, Docling extraction and verified theorem/result locations under literature/{pdf,markdown,references}/ before making citations or priority claims.

## Scope and manuscript layout

A short paper: problem and distinction from prior methods; concise objective and algorithm; meaningful mathematical statement(s); two figures plus a reproducible statistical comparison; limitations. Keep exhaustive synthetic galleries and derivations in supplementary material. This file is the **working research thesis**, not a finished paper.
