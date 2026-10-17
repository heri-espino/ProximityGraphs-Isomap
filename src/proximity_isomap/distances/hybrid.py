"""Finite hybrid dissimilarities for disconnected graphs.

This is not necessarily a metric; triangle inequalities need not hold.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.sparse.csgraph import shortest_path
from scipy.spatial.distance import cdist

from proximity_isomap.graphs.radius import RadiusGraph


@dataclass(frozen=True)
class HybridDissimilarities:
    """Targets for weighted stress, with explicit within-component pair mask."""

    target: NDArray[np.float64]
    same_component: NDArray[np.bool_]


def hybrid_dissimilarities(
    points: NDArray[np.floating], graph: RadiusGraph
) -> HybridDissimilarities:
    """Within components use graph shortest paths; otherwise ambient distances.

    Parameters
    ----------
    points:
        Exactly the points, in exactly the order, used to build ``graph``.
    graph:
        Radius graph weighted by Euclidean endpoint lengths.

    Notes
    -----
    This function cannot independently verify that ``points`` and ``graph``
    originate from the same data; callers must preserve order and identity.

    Returns
    -------
    HybridDissimilarities
        Full finite dissimilarity targets and a Boolean intracomponent mask.

    Raises
    ------
    ValueError
        If the point array has invalid shape, count, or entries.
    RuntimeError
        If supplied component labels contradict graph reachability.
    """
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or x.shape[0] != graph.adjacency.shape[0]:
        raise ValueError("point count and graph shape must match")
    if not np.isfinite(x).all():
        raise ValueError("points must be finite")

    same = graph.component_labels[:, None] == graph.component_labels[None, :]
    graph_dist = shortest_path(graph.adjacency, directed=False, unweighted=False)
    if not np.isfinite(graph_dist[same]).all():
        raise RuntimeError("a declared component contains unreachable vertices")
    ambient_dist = cdist(x, x)
    target = np.where(same, graph_dist, ambient_dist)
    np.fill_diagonal(target, 0.0)
    return HybridDissimilarities(target=target, same_component=same)
