"""Small mathematical invariants for rebuilt experiments, independent of old ZIP."""

import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "proximity_isomap" / "code"))
from research_runner import classical_mds, component_coordinates, multiple_sheets, stress  # noqa: E402


def test_mds_recovers_flat_pair_distances():
    """Classical MDS recovers full pair distances for planar points."""
    rng = np.random.default_rng(37)
    flat = rng.normal(size=(20, 2))
    y = classical_mds(squareform(pdist(flat)))
    assert np.allclose(pdist(y), pdist(flat), atol=1e-8)


def test_mst_diagnostic_radius_finds_two_components():
    """Artificial label-informed radius creates the expected two components."""
    x, flat, truth, radius = multiple_sheets(2, 24, 20261018)
    z, predicted = component_coordinates(x, radius)
    assert z.shape == (48, 2)
    assert len(np.unique(predicted)) == 2
    assert flat.shape == (48, 2)
    assert len(np.unique(truth)) == 2


def test_intrinsic_stress_is_zero_for_identical_flat_coordinates():
    """Analytic within-sheet ground truth is an exact evaluation target."""
    x, flat, truth, _ = multiple_sheets(1, 20, 20261018)
    wi, between = stress(x, flat, truth, flat.copy())
    assert wi < 1e-12
    assert between is None
