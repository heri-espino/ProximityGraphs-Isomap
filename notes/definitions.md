# Definitions and notation

**Status:** definitions (not claims of novelty)  
**Updated:** 2026-10-16

## DEF-0001: dataset and embedding

Let `X = (x_1, ..., x_n)` with `x_i in R^D`. An embedding consists of `Y = (y_1, ..., y_n)` with `y_i in R^d`, usually `d < D`. Euclidean distances in original and embedded spaces are `e_ij = ||x_i-x_j||_2` and `q_ij(Y) = ||y_i-y_j||_2`.

## DEF-0002: undirected radius graph

For `r > 0`, define `G_r=(V,E_r)` with `V={1,...,n}` and `(i,j) in E_r` exactly when `i != j` and `||x_i-x_j||_2 <= r`; assign edge weight `w_ij = ||x_i-x_j||_2`. This is an endpoint-distance rule. It is **not** the intersection graph of Euclidean balls of radius `r`, which connects at center distance at most `2r`.

## DEF-0003: component labels and graph geodesics

Let `c_i` be the connected component label of vertex `i`. Define `g_ij` as the weighted graph shortest-path length if `c_i=c_j`. For different components, `g_ij=+infinity`; an infinite value must not be handed directly to classical MDS.

## DEF-0004: hybrid dissimilarity

Define `delta_ij = g_ij` if `c_i=c_j`, otherwise `delta_ij=e_ij`. This is a finite, symmetric, nonnegative **dissimilarity**, not necessarily a metric. In particular, it may violate the triangle inequality. `delta_ii=0`.

## DEF-0005: normalized hybrid stress

Let `P_in={(i,j):i<j and c_i=c_j}` and `P_out={(i,j):i<j and c_i!=c_j}`. For a nonempty group `P`, define `S_P(Y) = [sum_(i,j)in P (q_ij(Y)-delta_ij)^2] / [sum_(i,j)in P delta_ij^2]` when its denominator is positive. If a group is empty or has zero denominator, it is omitted, not silently divided by zero. Let `alpha in [0,1]`. Define `L_alpha = [alpha*S_in*I_in+(1-alpha)*S_out*I_out] / [alpha*I_in+(1-alpha)*I_out]` if the denominator is nonzero, with `I_*` indicating a defined group stress. This explicitly handles degenerate component structures.

This objective is scale-sensitive in the embedding and nonconvex in `Y`. Optimizer, initialization and multistart strategy remain future work.

## Clarifying distinction

Third-point insertion cannot change the existence of a radius edge between two existing points, but distinct random edges are **not** generally independent because of shared random endpoints.
