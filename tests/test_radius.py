import numpy as np
import pytest

from proximity_isomap import radius_graph


def test_two_components_and_weighted_edges():
    x = np.array([[0.0, 0], [1.0, 0], [10.0, 0], [11.0, 0]])
    g = radius_graph(x, radius=1.1)
    assert g.n_components == 2
    assert g.n_edges == 2
    assert g.adjacency[0, 1] == pytest.approx(1.0)
    assert g.adjacency[0, 2] == 0


def test_edges_only_increase_with_radius():
    x = np.array([[0.0, 0], [1.0, 0], [2.2, 0], [5.0, 0]])
    small, big = radius_graph(x, 1.3), radius_graph(x, 3.0)
    assert small.n_components >= big.n_components
    a = set(zip(*small.adjacency.nonzero(), strict=True))
    b = set(zip(*big.adjacency.nonzero(), strict=True))
    assert a <= b


def test_third_point_cannot_change_existing_pair_edge():
    base = np.array([[0.0, 0], [1.0, 0]])
    extended = np.vstack([base, [[0.5, 0]]])
    assert radius_graph(base, 1.1).adjacency[0, 1] == 1.0
    assert radius_graph(extended, 1.1).adjacency[0, 1] == 1.0


def test_coincident_distinct_points_form_zero_weight_edge():
    x = np.array([[0.0, 0], [0.0, 0], [4.0, 0]])
    g = radius_graph(x, 0.5)
    assert g.n_edges == 1
    assert g.n_components == 2
    assert g.adjacency.nnz == 2


@pytest.mark.parametrize("radius", [0.0, -1.0, np.inf, np.nan])
def test_invalid_radius(radius):
    with pytest.raises(ValueError):
        radius_graph(np.array([[0.0]]), radius)
