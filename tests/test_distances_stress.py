import numpy as np
import pytest

from proximity_isomap import hybrid_dissimilarities, normalized_hybrid_stress, radius_graph


def test_hybrid_distances_use_geodesic_within_and_euclidean_between():
    x = np.array([[0., 0.], [1., 0.], [1., 1.], [8., 8.]])
    h = hybrid_dissimilarities(x, radius_graph(x, 1.1))
    assert h.target[0, 2] == pytest.approx(2.0)
    assert h.target[0, 3] == pytest.approx(np.sqrt(128.0))
    assert h.same_component[0, 2]
    assert not h.same_component[0, 3]
    assert np.allclose(h.target, h.target.T)


def test_euclidean_coordinates_have_zero_stress_for_simple_components():
    x = np.array([[0., 0.], [1., 0.], [10., 0.], [11., 0.]])
    h = hybrid_dissimilarities(x, radius_graph(x, 1.1))
    report = normalized_hybrid_stress(x, h, alpha=0.7)
    assert report.combined == pytest.approx(0.0)
    assert report.within_pairs == 2
    assert report.between_pairs == 4


def test_all_isolated_vertices_can_use_between_stress_only():
    x = np.array([[0., 0.], [10., 0.], [20., 0.]])
    h = hybrid_dissimilarities(x, radius_graph(x, 0.5))
    report = normalized_hybrid_stress(x, h, alpha=0.7)
    assert report.within is None
    assert report.between == pytest.approx(0.0)
    with pytest.raises(ValueError):
        normalized_hybrid_stress(x, h, alpha=1.0)


def test_single_component_can_use_within_stress_only():
    x = np.array([[0., 0.], [1., 0.]])
    h = hybrid_dissimilarities(x, radius_graph(x, 1.1))
    report = normalized_hybrid_stress(x, h, alpha=0.25)
    assert report.between is None
    assert report.combined == pytest.approx(0.0)


def test_shape_mismatch_rejected():
    x = np.array([[0., 0.], [1., 0.]])
    h = hybrid_dissimilarities(x, radius_graph(x, 1.1))
    with pytest.raises(ValueError):
        normalized_hybrid_stress(np.array([[0.]]), h)
