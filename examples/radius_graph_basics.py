"""Quick smoke example; run after editable installation."""

import numpy as np

from proximity_isomap import hybrid_dissimilarities, normalized_hybrid_stress, radius_graph

x = np.array([[0., 0.], [1., 0.], [8., 0.], [9., 0.]])
g = radius_graph(x, radius=1.5)
h = hybrid_dissimilarities(x, g)
print(f"Components: {g.n_components}, edges: {g.n_edges}")
print("Hybrid dissimilarities:\n", h.target)
print("Original embedding stress:", normalized_hybrid_stress(x, h, alpha=0.5))
