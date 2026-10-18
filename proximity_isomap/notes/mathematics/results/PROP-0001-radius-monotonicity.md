# PROP-0001: radius monotonicity and connectivity threshold

**Status:** proven (standard graph-geometric facts; not new)  
**Dependencies:** DEF-0002, DEF-0003

## Statement

For a fixed finite Euclidean point set and `0 < r_1 <= r_2`:

1. `E_(r_1) subseteq E_(r_2)`.
2. The number of connected components cannot increase as `r` grows.
3. For any pair connected in `G_(r_1)`, `g_(r_2)(i,j) <= g_(r_1)(i,j)`.
4. Assuming a connected weighted complete Euclidean graph on the point indices, the smallest radius for which `G_r` is connected equals the maximum edge length in a Euclidean minimum spanning tree. For `n=1`, interpret this threshold as zero.

## Proof

1. If the endpoint distance is at most `r_1`, it is also at most `r_2`; therefore each edge at the smaller radius survives.
2. Adding edges cannot split a connected component, though it can merge components.
3. Any path in `G_(r_1)` is also a path of the same edge weight in `G_(r_2)`; the minimization set only becomes larger.
4. Let `T` be an MST and let `b` be its longest edge length. At radius `b`, every MST edge is present and so the graph is connected. Conversely, if `G_r` is connected, it has a spanning tree using edges of length at most `r`. The MST bottleneck property guarantees some MST has maximum edge length no greater than `r`; all MSTs have the same bottleneck value in a fixed graph (including ties). Thus `b <= r`.

## Limits

None of these monotonicities says that a larger radius **reduces error against intrinsic manifold geodesics**; shortcuts can make distortion worse. Duplicate points yield zero-weight edges and should be included in implementation tests.
