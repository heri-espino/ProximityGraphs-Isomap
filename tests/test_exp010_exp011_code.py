"""Lightweight checks for native EXP-010 and EXP-011 generators."""
from __future__ import annotations

import runpy
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def _script(number: str, slug: str):
    return runpy.run_path(str(ROOT / "proximity_isomap" / "code" / f"{number}-{slug}" / "run.py"))


def test_exp010_cylinder_and_rings_have_distinct_support_counts():
    mod = _script("010", "radius_density_and_rings")
    cylinder, cylinder_labels = mod["cylinder"](9, 6)
    rings, ring_labels = mod["rings"](18)
    assert cylinder.shape == (54, 3)
    assert rings.shape == (90, 3)
    assert len(np.unique(cylinder_labels)) == 1
    assert len(np.unique(ring_labels)) == 5
    remaining = 54 - np.searchsorted(mod["mst_deaths"](cylinder), 0.5, side="right")
    assert int(remaining) == 54


def test_exp011_detects_five_separate_rings_and_fits_componentwise_knn():
    mod = _script("011", "isomap_baselines")
    x, truth, intrinsic, kind = mod["sample"]("rings", 20261018, True)
    detected, radius, policy = mod["components"](x, "rings", 5)
    assert x.shape[1] == 3 and kind == "circle"
    assert len(np.unique(detected)) == 5
    assert policy == "fixed_radius"
    y = mod["piecewise"](x, detected, "knn", radius)
    assert y.shape == (len(x), 2)
    assert np.isfinite(y).all()
    score = mod["metrics"](x, y, truth, intrinsic, kind)
    assert score["intrinsic_stress"] is not None and score["intrinsic_stress"] >= 0
