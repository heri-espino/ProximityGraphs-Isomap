"""Research utilities for radius-graph and disconnected-manifold baselines.

Experimental package: no convergence guarantee or novel algorithm is claimed.
"""

from proximity_isomap.distances.hybrid import HybridDissimilarities, hybrid_dissimilarities
from proximity_isomap.embedding.stress import StressBreakdown, normalized_hybrid_stress
from proximity_isomap.graphs.radius import RadiusGraph, radius_graph

__all__ = [
    "HybridDissimilarities",
    "RadiusGraph",
    "StressBreakdown",
    "hybrid_dissimilarities",
    "normalized_hybrid_stress",
    "radius_graph",
]
