"""Small unit tests: do not compute the 14-scenario full benchmark."""
from __future__ import annotations

import runpy
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics import adjusted_rand_score

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "proximity_isomap" / "code" / "013-classical_multicomponent_dashboards" / "run.py"


def module():
    return runpy.run_path(str(SOURCE))


def test_far_near_nonintersecting_for_all_families():
    m = module()
    for family in m["FAMILIES"]:
        far, lab, _, _, f = m["place_clouds"](family, "far", 25, 314159)
        near, lab2, _, _, n = m["place_clouds"](family, "near", 25, 314159)
        assert np.array_equal(lab, lab2)
        assert f["observed_gap"] > n["observed_gap"] > 0
        assert far.shape == near.shape
        for i in np.unique(lab):
            for j in np.unique(lab):
                if i < j:
                    assert cdist(near[lab == i], near[lab == j]).min() > 0


def test_union_knn_and_oracle_reference_partition():
    m = module()
    x, truth, _, _, _ = m["place_clouds"]("rings", "far", 36, 137)
    graph = m["sym_knn"](x, 5)
    assert (graph - graph.T).nnz == 0
    assert np.all(np.isfinite(graph.data))
    pred = m["mst_cut"](x, 3)
    assert len(np.unique(pred)) == 3
    assert adjusted_rand_score(truth, pred) >= 0.5


def test_componentwise_embedding_has_finite_scores():
    m = module()
    x, truth, params, kinds, _ = m["place_clouds"]("springs", "far", 35, 42)
    detect = m["partition_from_graph"](m["sym_knn"](x, 7))
    y = m["piecewise"](x, detect, "knn", 10, 0.5)
    g = m["true_geodesics"](x, truth, params, kinds)
    values = m["score"](x, y, truth, g)
    assert y.shape == (len(x), 2)
    assert np.isfinite(y).all()
    assert 0 <= values["trustworthiness"] <= 1
    assert np.isfinite(values["intrinsic_stress"])
    assert values["hull_overlaps"] >= 0


def test_3x3_layouts_are_exactly_nine():
    m = module()
    assert len(m["ISOMAP"]) == len(set(m["ISOMAP"])) == 9
    assert len(m["GENERAL"]) == len(set(m["GENERAL"])) == 9
    assert m["ISOMAP"][4] == m["GENERAL"][4] == "Componentwise kNN Isomap"
    assert len(m["METHODS"]) == 12
