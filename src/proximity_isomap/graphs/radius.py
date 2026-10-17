"""Pairwise-local undirected radius graph with Euclidean edge weights."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree


@dataclass(frozen=True)
class RadiusGraph:
    """Weighted adjacency and component labels for a fixed-radius graph.

    Adjacency is a symmetric CSR matrix with no self-edges. Stored zero values
    represent legitimate edges between coincident *distinct* observations.
    """

    adjacency: csr_matrix
    component_labels: NDArray[np.int32]
    radius: float

    @property
    def n_components(self) -> int:
        """Number of undirected connected components, including isolated vertices."""
        return int(np.unique(self.component_labels).size)

    @property
    def n_edges(self) -> int:
        """Number of undirected edges (each edge appears twice in the matrix)."""
        return self.adjacency.nnz // 2


def radius_graph(points: NDArray[np.floating], radius: float) -> RadiusGraph:
    """Connect distinct points iff their Euclidean distance is <= ``radius``.

    The graph is *not* an intersection graph of balls of radius ``radius``.
    Adding a third point never changes an existing pair's adjacency.

    Parameters
    ----------
    points:
        Finite ``(n, D)`` array, ``n >= 1`` and ``D >= 1``.
    radius:
        Positive finite cutoff in original coordinate units.

    Returns
    -------
    RadiusGraph
        Sparse Euclidean-weighted adjacency, component labels, and cutoff.

    Raises
    ------
    ValueError
        If points or radius do not satisfy the finite-shape constraints.
    """
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or min(x.shape) < 1 or not np.isfinite(x).all():
        raise ValueError("points must be a nonempty finite 2-D array")
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be positive and finite")

    pairs = cKDTree(x).query_pairs(r=radius, output_type="ndarray")
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    if len(pairs):
        lengths = np.linalg.norm(x[pairs[:, 0]] - x[pairs[:, 1]], axis=1)
        rows = np.concatenate((pairs[:, 0], pairs[:, 1]))
        cols = np.concatenate((pairs[:, 1], pairs[:, 0]))
        values = np.concatenate((lengths, lengths))
    else:
        rows = cols = np.empty(0, dtype=np.int64)
        values = np.empty(0, dtype=float)

    adjacency = csr_matrix((values, (rows, cols)), shape=(len(x), len(x)))
    _, labels = connected_components(adjacency, directed=False)
    return RadiusGraph(adjacency, labels, float(radius))
