"""Rebuilt reproducible experiments EXP-001–008; not historical code recovery.

Every run stores input data, exact metrics, a manifest, publication-style PNG/SVG
figures, and an automatically maintained experiment note. Synthetic truth is used
for *evaluation* and, where marked, an explicitly oracle connectivity threshold.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn
from scipy.optimize import minimize
from scipy.sparse.csgraph import minimum_spanning_tree, shortest_path
from scipy.spatial.distance import cdist, pdist, squareform
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

from proximity_isomap import radius_graph

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "proximity_isomap"
SLUGS = {
    1: "001-radius_filtration",
    2: "002-hybrid_mds",
    3: "003-wide_radius_grid",
    4: "004-radius_transfer",
    5: "005-paired_manifolds",
    6: "006-rotated_swiss_rolls",
    7: "007-component_alignment",
    8: "008-multiple_swiss_rolls",
}


def setup_colors() -> list[str]:
    """Use the version-pinned ContrastColors library for all saved figures.

    Returns
    -------
    list[str]
        Categorical palette using the library's original Okabe--Ito colors.

    Raises
    ------
    ImportError
        When the required user-owned ContrastColors package is not installed.
    """
    import contrastcolors as cc

    cc.set_style("heri", palette="okabe-ito", font="DejaVu Sans", use_tex=False)
    return list(cc.color_palette("okabe-ito", as_hex=True))


def sample_sheet(kind: str, n: int, seed: int, skew: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Sample an isometric 2D strip embedded as a Swiss roll or S-like curve.

    Parameters
    ----------
    kind : str
        Either "swiss" or "s"; only noiseless synthetic families are supported.
    n : int
        Positive observations per sheet.
    seed : int
        Deterministic sheet seed.
    skew : bool
        Bias the first intrinsic coordinate toward one end when true.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Ambient (n,3) and analytical intrinsic (n,2) coordinates.
    """
    rng = np.random.default_rng(seed)
    u = rng.beta(2.0, 5.0, n) if skew else rng.random(n)
    h = rng.uniform(-5, 5, n)
    if kind == "swiss":
        t = (1.5 + 3.0 * u) * np.pi
        xyz = np.column_stack((t * np.cos(t), h, t * np.sin(t)))
        s = 0.5 * (t * np.sqrt(1 + t * t) + np.arcsinh(t))
    elif kind == "s":
        t = (u - 0.5) * 2.8 * np.pi
        xyz = np.column_stack((np.sin(t), h, np.sign(t) * (np.cos(t) - 1)))
        s = t
    else:
        raise ValueError(f"Unknown manifold: {kind}")
    return xyz, np.column_stack((s, h))


def multiple_sheets(
    k: int, n: int, seed: int, *, kind: str = "swiss",
    rotated: bool = True, skew: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Construct genuinely disjoint sheets and a label-informed radius diagnostic.

    Parameters
    ----------
    k : int
        Number of generating sheets.
    n : int
        Samples per sheet.
    seed : int
        Generator seed.
    kind : str
        Manifold family.
    rotated : bool
        Whether later sheets have distinct 3D orientations.
    skew : bool
        Whether to skew the sampling parameter.

    Returns
    -------
    tuple
        Ambient points, intrinsic coordinates, true labels, oracle MST radius.
        The oracle radius may not be used to claim unsupervised selection.
    """
    xx, zz = [], []
    max_edge = 0.0
    for j in range(k):
        x, z = sample_sheet(kind, n, seed + j * 97, skew=skew)
        if rotated and j:
            angle = np.deg2rad(35 + 27 * j)
            yaw = np.deg2rad(50 + 19 * j)
            a = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)],
                          [0, np.sin(angle), np.cos(angle)]])
            b = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                          [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
            x = (x - x.mean(axis=0)) @ (b @ a).T
        edges = minimum_spanning_tree(cdist(x, x)).data
        max_edge = max(max_edge, float(edges.max()) if len(edges) else 0.0)
        xx.append(x)
        zz.append(z)
    radius = max_edge * (1 + 1e-7)
    for j in range(1, k):
        xx[j] = xx[j].copy()
        xx[j][:, 0] += float(xx[j - 1][:, 0].max() + 1.5 * radius - xx[j][:, 0].min())
    return np.vstack(xx), np.vstack(zz), np.repeat(np.arange(k), n), radius


def classical_mds(distance: np.ndarray) -> np.ndarray:
    """Embed a finite metric's squared-distance Gram matrix into 2D.

    Parameters
    ----------
    distance : np.ndarray
        Symmetric finite square dissimilarity matrix.

    Returns
    -------
    np.ndarray
        Centered (n,2) classical-MDS coordinates.
    """
    n = len(distance)
    d2 = distance**2
    gram = -0.5 * (d2 - d2.mean(axis=0)[None, :] -
                   d2.mean(axis=1)[:, None] + d2.mean())
    values, vectors = np.linalg.eigh(gram)
    values = np.maximum(values[-2:], 0)
    return vectors[:, -2:] * np.sqrt(values)


def component_coordinates(x: np.ndarray, radius: float) -> tuple[np.ndarray, np.ndarray]:
    """Independently embed each radius-graph component by geodesic classical MDS.

    Parameters
    ----------
    x : np.ndarray
        Ambient point cloud.
    radius : float
        Positive graph cutoff.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Local coordinates (n,2) and graph component labels.
    """
    graph = radius_graph(x, radius)
    labels = graph.component_labels
    embedded = np.zeros((len(x), 2))
    for lab in np.unique(labels):
        ids = np.flatnonzero(labels == lab)
        if len(ids) <= 1:
            continue
        distance = shortest_path(graph.adjacency[ids, :][:, ids], directed=False)
        if not np.isfinite(distance).all():
            raise RuntimeError("Internal graph-component shortest path is not finite")
        embedded[ids] = classical_mds(distance)
    return embedded, labels


def hybrid_coordinates(x: np.ndarray, radius: float, *, alpha: float = 0.5,
                       iterations: int = 75) -> tuple[np.ndarray, int]:
    """Approximate hybrid dissimilarities with one-start metric SMACOF MDS.

    Parameters
    ----------
    x : np.ndarray
        Ambient observations.
    radius : float
        Radius for graph shortest paths.
    alpha : float
        Interpolation weight on within-component path distances, not the
        weighted-stress alpha of the historical EXP-002 optimizer.
    iterations : int
        Max SMACOF iterations.

    Returns
    -------
    tuple[np.ndarray, int]
        Global 2D coordinates and graph-component count.

    Notes
    -----
    This reconstructed baseline is NOT mathematically identical to the
    unavailable historical weighted-hybrid-MDS optimizer.
    """
    graph = radius_graph(x, radius)
    ambient = squareform(pdist(x))
    geodesic = shortest_path(graph.adjacency, directed=False)
    within = graph.component_labels[:, None] == graph.component_labels[None, :]
    d = ambient.copy()
    d[within] = alpha * geodesic[within] + (1 - alpha) * ambient[within]
    mds = MDS(n_components=2, dissimilarity="precomputed", metric=True,
              n_init=1, max_iter=iterations, random_state=0)
    return mds.fit_transform(d), graph.n_components


def rigid_align(
    x: np.ndarray, local: np.ndarray, labels: np.ndarray, *,
    separated: bool, maxiter: int,
) -> tuple[np.ndarray, float]:
    """Align componentwise Isomap using rigid 2D poses and optional x-strip gaps.

    Parameters
    ----------
    x : np.ndarray
        Ambient observations.
    local : np.ndarray
        Independently computed Isomap coordinates.
    labels : np.ndarray
        Graph component identifiers.
    separated : bool
        Impose an ordered positive horizontal gap between all components.
    maxiter : int
        Bound for local nonconvex anchor optimization.

    Returns
    -------
    tuple[np.ndarray, float]
        Globally aligned (n,2) coordinates and achieved minimum x-strip gap.

    Notes
    -----
    Uses a small deterministic anchor subset in fitting, then evaluates
    stresses on ALL pairs. Constrained mode is a feasible pose heuristic,
    NOT the globally optimal separation-distortion frontier.
    """
    groups = [np.flatnonzero(labels == v) for v in np.unique(labels)]
    if len(groups) == 1:
        return local.copy(), float("nan")
    pca = PCA(n_components=2).fit_transform(x)
    centers = np.array([pca[g].mean(axis=0) for g in groups])
    pieces = [local[g] - local[g].mean(axis=0) for g in groups]
    picked = [np.unique(np.linspace(0, len(g)-1, min(10, len(g)),
                                    dtype=int)) for g in groups]
    pairs = [(i, j, cdist(x[groups[i][picked[i]]], x[groups[j][picked[j]]]))
             for i in range(len(groups)) for j in range(i + 1, len(groups))]
    norm = sum(float((d*d).sum()) for _, _, d in pairs)
    initial = np.r_[np.zeros(len(groups) - 1),
                    (centers[1:] - centers[0]).reshape(-1)]

    def decode(p: np.ndarray) -> list[np.ndarray]:
        ang = np.r_[0, p[:len(groups) - 1]]
        shifts = np.vstack((np.zeros(2), p[len(groups) - 1:].reshape(-1, 2)))
        placed = []
        for block, a, t in zip(pieces, ang, shifts, strict=True):
            c, s = np.cos(a), np.sin(a)
            placed.append(block @ np.array([[c, -s], [s, c]]) + t)
        return placed

    def loss(p: np.ndarray) -> float:
        placed = decode(p)
        return sum(float(((cdist(placed[i][picked[i]],
                                 placed[j][picked[j]]) - d)**2).sum())
                   for i, j, d in pairs) / norm

    opt = minimize(loss, initial, method="L-BFGS-B", options={"maxiter": maxiter})
    placed = decode(opt.x)
    gap = float("nan")
    if separated:
        positive = [float(np.median(pdist(p))) for p in pieces if len(p) > 1]
        target = 0.08 * float(np.median(positive))
        # Apply cumulative horizontal shifts, preserving all internal geometry.
        for j in range(1, len(placed)):
            required = placed[j-1][:, 0].max() + target
            placed[j] += np.array([required - placed[j][:, 0].min(), 0.0])
        gap = min(float(placed[j][:, 0].min() - placed[j-1][:, 0].max())
                  for j in range(1, len(placed)))
        if gap < target - 1e-8:
            raise RuntimeError("Non-overlap invariant failed")
    output = np.zeros_like(local)
    for ids, block in zip(groups, placed, strict=True):
        output[ids] = block
    return output - output.mean(axis=0), gap


def stress(x: np.ndarray, flat: np.ndarray, truth: np.ndarray,
           y: np.ndarray) -> tuple[float, float | None]:
    """Evaluate exact intrinsic within-sheet and ambient cross-sheet root stress.

    Parameters
    ----------
    x : np.ndarray
        Original ambient observations.
    flat : np.ndarray
        Analytical intrinsic strip coordinates for each generating manifold.
    truth : np.ndarray
        Synthetic generating-sheet identifiers (evaluation only).
    y : np.ndarray
        Projected low-dimensional points.

    Returns
    -------
    tuple[float, float | None]
        Normalized within-root-stress and between ambient-root-stress.
        Between stress is None when there is one manifold.
    """
    i, j = np.triu_indices(len(x), 1)
    same = truth[i] == truth[j]
    predicted = np.linalg.norm(y[i]-y[j], axis=1)
    wanted = np.linalg.norm(flat[i[same]] - flat[j[same]], axis=1)
    wi = float(np.linalg.norm(predicted[same] - wanted) / np.linalg.norm(wanted))
    if same.all():
        return wi, None
    cross = np.linalg.norm(x[i[~same]]-x[j[~same]], axis=1)
    out = float(np.linalg.norm(predicted[~same] - cross) / np.linalg.norm(cross))
    return wi, out


def method_fit(x: np.ndarray, flat: np.ndarray, truth: np.ndarray,
               radius: float, *, quick: bool) -> tuple[dict[str, np.ndarray], list[dict]]:
    """Fit fair-to-sample named baseline panels, keeping their caveats explicit.

    Parameters
    ----------
    x : np.ndarray
        Ambient data.
    flat : np.ndarray
        True intrinsic generating coordinates for evaluation.
    truth : np.ndarray
        Generating manifold identifiers for evaluation.
    radius : float
        Diagnostic radius.
    quick : bool
        Use smaller iteration budgets in smoke mode.

    Returns
    -------
    tuple
        Named 2D projections and row dictionaries for CSV metrics.
    """
    local, labels = component_coordinates(x, radius)
    hybrid, count = hybrid_coordinates(x, radius, iterations=25 if quick else 70)
    free, free_gap = rigid_align(x, local, labels, separated=False,
                                 maxiter=16 if quick else 80)
    separate, gap = rigid_align(x, local, labels, separated=True,
                                maxiter=16 if quick else 80)
    predictions = {
        "PCA": PCA(n_components=2).fit_transform(x),
        "Hybrid_MDS": hybrid,
        "Component_Isomap_free": free,
        "Component_Isomap_separated": separate,
    }
    rows = []
    for name, y in predictions.items():
        within, between = stress(x, flat, truth, y)
        rows.append({"method": name, "within_intrinsic_root_stress": within,
                     "between_ambient_root_stress": between,
                     "n_graph_components": count,
                     "horizontal_gap": gap if name.endswith("separated") else
                     free_gap if name.endswith("free") else None})
    return predictions, rows


def figure_overview(x: np.ndarray, labels: np.ndarray, fit: dict[str, np.ndarray],
                    path: Path, title: str, colors: list[str]) -> None:
    """Save an original-3D versus 2D-panels figure in PNG and SVG.

    Parameters
    ----------
    x : np.ndarray
        Ambient 3D observations.
    labels : np.ndarray
        Generating component identifiers, used for consistent coloring.
    fit : dict[str, np.ndarray]
        Named 2D projections.
    path : Path
        Image path base without suffix.
    title : str
        Descriptive figure heading.
    colors : list[str]
        Colors chosen through ContrastColors.

    Returns
    -------
    None
        Saves two vector/raster figure formats.
    """
    fig = plt.figure(figsize=(16, 6), layout="constrained")
    axs = [fig.add_subplot(1, len(fit)+1, 1, projection="3d")]
    axs.extend(fig.add_subplot(1, len(fit)+1, c+2)
               for c in range(len(fit)))
    for k in np.unique(labels):
        ids = labels == k
        axs[0].scatter(*x[ids].T, s=7, color=colors[int(k) % len(colors)],
                       alpha=0.8, depthshade=False)
    axs[0].set_title("Original 3D", fontsize=10)
    axs[0].view_init(elev=21, azim=-61)
    for ax, (name, y) in zip(axs[1:], fit.items(), strict=True):
        for k in np.unique(labels):
            ids = labels == k
            ax.scatter(*y[ids].T, s=7, color=colors[int(k) % len(colors)], alpha=.85)
        ax.set_title(name.replace("_", " "), fontsize=9)
        ax.set_aspect("equal", adjustable="datalim")
    fig.suptitle(title)
    for ext in ("png", "svg"):
        fig.savefig(path.with_suffix("." + ext), dpi=170)
    plt.close(fig)


def save_chart(rows: list[dict], key: str, metric: str,
               path: Path, title: str) -> None:
    """Render a numeric stress curve with the pinned ContrastColors style.

    Parameters
    ----------
    rows : list[dict]
        Complete metric data rows.
    key : str
        Independent-coordinate column.
    metric : str
        Response column.
    path : Path
        File prefix.
    title : str
        Figure title.

    Returns
    -------
    None
        PNG and SVG charts.
    """
    fig, ax = plt.subplots(figsize=(8.7, 4.3), layout="constrained")
    categories = list(dict.fromkeys(str(row.get("method", "graph")) for row in rows))
    for method in categories:
        sub = [row for row in rows if str(row.get("method", "graph")) == method
               and row.get(metric) is not None]
        if sub:
            ax.plot([float(r[key]) for r in sub],
                    [float(r[metric]) for r in sub], marker="o", label=method)
    ax.set(xlabel=key.replace("_", " "), ylabel=metric.replace("_", " "),
           title=title)
    ax.legend(fontsize=8)
    for ext in ("png", "svg"):
        fig.savefig(path.with_suffix("." + ext), dpi=180)
    plt.close(fig)


def git_sha() -> str | None:
    """Read the repository's source commit hash, if available.

    Returns
    -------
    str or None
        Full SHA for an authenticated Git checkout or None in a detached archive.
    """
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def write_rows(path: Path, rows: list[dict]) -> None:
    """Write a uniform table, preserving empty values for undefined stresses.

    Parameters
    ----------
    path : Path
        CSV path.
    rows : list[dict]
        Nonempty list of rows with compatible columns.

    Returns
    -------
    None
        CSV text written to path.
    """
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(index: int, *, seed: int, quick: bool,
                   label: str) -> dict:
    """Run a reconstructed research question and archive its outputs.

    Parameters
    ----------
    index : int
        Experiment ID in 1..8.
    seed : int
        Generating RNG seed.
    quick : bool
        Smoke mode using smaller samples and optimization budget.
    label : str
        Shared run label across all eight experiments.

    Returns
    -------
    dict
        Machine-readable run metadata and paths. All outputs are immutable.
    """
    if index not in SLUGS:
        raise ValueError("Unknown experiment index")
    slug = SLUGS[index]
    dest = RESEARCH / "results" / slug / "runs" / label
    fig = RESEARCH / "figures" / slug / "runs" / label
    if dest.exists() or fig.exists():
        raise FileExistsError(f"Refusing to overwrite an existing run: {label}")
    dest.mkdir(parents=True)
    fig.mkdir(parents=True)
    colors = setup_colors()
    n = 36 if quick else 180
    chart_rows = []
    rows = []
    x = flat = labels = None
    saved_fits = {}
    if index == 1:
        x, flat, labels, radius = multiple_sheets(1, n, seed)
        truth = squareform(pdist(flat))
        for r in np.linspace(radius * 0.25, radius * 1.8, 9 if quick else 19):
            graph = radius_graph(x, float(r))
            dist = shortest_path(graph.adjacency, directed=False)
            ii, jj = np.triu_indices(len(x), 1)
            connected = graph.component_labels[ii] == graph.component_labels[jj]
            err = float(np.sqrt(np.mean((dist[ii[connected], jj[connected]] -
                                         truth[ii[connected], jj[connected]])**2))) if connected.any() else None
            rows.append({"radius": float(r), "n_components": graph.n_components,
                         "n_edges": graph.n_edges, "conditional_graph_rmse": err,
                         "n_finite_pairs": int(connected.sum())})
        save_chart(rows, "radius", "conditional_graph_rmse", fig/"radius_sweep",
                   "EXP-001: graph-error versus radius (changing finite pairs)")
    elif index == 3:
        x, flat, labels, radius = multiple_sheets(1, 50 if quick else 100, seed)
        for r in np.geomspace(radius * .1, radius * 2, 8 if quick else 20):
            y, count = hybrid_coordinates(x, float(r), iterations=20 if quick else 55)
            wi, _ = stress(x, flat, labels, y)
            rows.append({"radius": float(r), "method": "Hybrid_MDS",
                         "n_graph_components": count,
                         "within_intrinsic_root_stress": wi})
        save_chart(rows, "radius", "within_intrinsic_root_stress", fig/"radius_stress",
                   "EXP-003: true intrinsic stress; radius not held out")
    elif index == 4:
        # Fixed radius derived from separate development Swiss data; explicitly
        # oracle-selected using analytic intrinsic truth, then frozen at evaluation.
        multipliers = np.linspace(.6, 1.4, 5 if quick else 9)
        dev = []
        for factor in multipliers:
            sample_errors = []
            for j in range(2 if quick else 5):
                a, z, lab, r = multiple_sheets(1, 44 if quick else 85, seed+1000+j)
                y, _ = hybrid_coordinates(a, r*float(factor),
                                          iterations=15 if quick else 40)
                sample_errors.append(stress(a, z, lab, y)[0])
            dev.append(float(np.mean(sample_errors)))
        factor = float(multipliers[int(np.argmin(dev))])
        for kind in ("swiss", "s"):
            for skew in (False, True):
                for j in range(2 if quick else 8):
                    x0, z0, lab0, r0 = multiple_sheets(
                        1, 44 if quick else 85, seed+4000+j+int(skew)*900+
                        (0 if kind == "swiss" else 2000), kind=kind, skew=skew)
                    fits = {"PCA": PCA(n_components=2).fit_transform(x0),
                            "Hybrid_MDS": hybrid_coordinates(
                                x0, r0*factor, iterations=15 if quick else 40)[0]}
                    for name, y in fits.items():
                        rows.append({"family": kind, "density": "skew" if skew else "uniform",
                                     "sample": j, "method": name,
                                     "within_intrinsic_root_stress": stress(x0,z0,lab0,y)[0],
                                     "development_oracle_factor": factor})
        groups = {}
        for r in rows:
            key = (r["family"], r["density"], r["method"])
            groups.setdefault(key, []).append(r["within_intrinsic_root_stress"])
        chart_rows = [{"regime": i, "method": method,
                       "mean_within_intrinsic_stress": float(np.mean(vals))}
                      for i, ((kind, skew, method), vals) in
                      enumerate(sorted(groups.items()))]
        fig2, ax = plt.subplots(figsize=(8.7,4.3), layout="constrained")
        for name in ("PCA", "Hybrid_MDS"):
            vals = [(k, v) for k,v in groups.items() if k[2]==name]
            ax.plot(range(len(vals)), [np.mean(v) for k,v in vals],
                    marker="o", label=name)
            ax.set_xticks(range(len(vals)),
                          [f"{k[0]}-{k[1]}" for k,v in vals])
        ax.set(ylabel="Mean within-sheet intrinsic stress", title="EXP-004: held-out density/geometry")
        ax.legend()
        for ext in ("png","svg"):
            fig2.savefig((fig/"density_transfer").with_suffix("." + ext), dpi=180)
        plt.close(fig2)
        x, flat, labels = x0,z0,lab0
    elif index in (2,5,6,7,8):
        scenarios = (
            [(k, "swiss", True, f"rolls_{k:02d}") for k in range(1, 7)]
            if index == 8 else
            [(2, "swiss", False, "swiss_pair"), (2, "s", False, "s_curve_pair")]
            if index == 5 else
            [(2, "swiss", False, "parallel"), (2, "swiss", True, "rotated")]
            if index == 6 else
            [(2, "swiss", True, "rotated_pair")]
            if index == 7 else
            [(1, "swiss", True, "single"), (2, "swiss", True, "pair")]
        )
        for k, kind, rotated, scenario in scenarios:
            x, flat, labels, radius = multiple_sheets(
                k, n if index != 2 else (40 if quick else 90),
                seed, kind=kind, rotated=rotated)
            fit, scores = method_fit(x, flat, labels, radius, quick=quick)
            for row in scores:
                rows.append({"n_rolls": k, "n_points": len(x),
                             "scenario": scenario, "radius": radius, **row})
            saved_fits = {f"{scenario}_{name}": y for name, y in fit.items()}
            figure_overview(x, labels, fit, fig/scenario,
                            f"EXP-{index:03d}: {scenario}", colors)
        if index == 8:
            save_chart(rows, "n_rolls", "within_intrinsic_root_stress",
                       fig/"within_stress_vs_count",
                       "EXP-008: intracomponent geometry as K grows")
    else:
        raise RuntimeError("Experiment not implemented")
    if x is not None and flat is not None and labels is not None:
        np.savez_compressed(dest/"coordinates.npz", x=x, intrinsic=flat, labels=labels,
                            **saved_fits)
    write_rows(dest/"metrics.csv", rows)
    if chart_rows:
        write_rows(dest/"aggregates.csv", chart_rows)
    metadata = {
        "experiment_id": f"EXP-{index:03d}", "slug": slug,
        "run_label": label, "generated_utc": datetime.now(UTC).isoformat(),
        "seed": seed, "quick": quick, "git_sha": git_sha(),
        "python": platform.python_version(), "numpy": np.__version__,
        "scipy": scipy.__version__, "sklearn": sklearn.__version__,
        "contrastcolors": __import__("contrastcolors").__version__,
        "methods": "reconstructed_from_documented_questions_not_original_2026_code",
        "ground_truth_use": "analytic geodesic evaluation; label-informed connectivity for K>=2",
        "selection_caveat": "EXP-004 development radius uses analytic ground truth; not unsupervised",
        "solver_caveat": "single-start SMACOF; rigid alignment nonconvex local anchor fit",
        "rows": len(rows),
    }
    (dest/"metadata.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    checks = {}
    for path in list(dest.glob("*")) + list(fig.glob("*")):
        if path.is_file():
            checks[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (dest/"sha256.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
    if quick:
        return metadata
    # Update a single canonical experiment note, preserving its historical
    # narrative but adding new figures from the actual current numerical run.
    note = RESEARCH/"notes"/slug/"README.md"
    old = note.read_text(encoding="utf-8")
    marker = "<!-- CURRENT-REPRODUCTION: replace this section on each new run -->"
    if marker in old:
        old = old.split(marker)[0].rstrip() + "\n"
    pngs = sorted(fig.glob("*.png"))
    visuals = "\n".join(
        f"![New {index:03d} plot: {p.stem.replace('_',' ')}]"
        f"(../../figures/{slug}/runs/{label}/{p.name})"
        for p in pngs
    )
    display = "\n".join(f"| {r.get('n_rolls','-')} | {r.get('method','graph')} | "
                        f"{r.get('within_intrinsic_root_stress',r.get('conditional_graph_rmse','-'))} | "
                        f"{r.get('between_ambient_root_stress','-')} |"
                        for r in rows[:20])
    note.write_text(
        old + f"\n\n{marker}\n\n## Latest *newly computed* experiment\n\n"
        f"Run: **{label}**; mode: **{'smoke' if quick else 'full'}**; seed: **{seed}**. "
        "This run REBUILDS the research question using the current implementation; "
        "it is **not the recovered historical algorithm or an independent novelty claim**. "
        f"Original arrays and metrics: [results](../../results/{slug}/runs/{label}/metrics.csv); "
        f"[metadata](../../results/{slug}/runs/{label}/metadata.json).\n\n"
        "| K | Method | Within intrinsic stress / diagnostic RMSE | Between ambient stress |\n"
        "|---:|---|---:|---:|\n" + display + "\n\n"
        f"{visuals}\n", encoding="utf-8")
    return metadata


def main(index: int | None = None) -> None:
    """Run all or exactly one experiment using a shared output label.

    Parameters
    ----------
    index : int or None
        Optional fixed experiment ID for per-experiment wrappers.

    Returns
    -------
    None
        Writes immutable outputs and Markdown updates.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Small smoke dataset, not research evidence")
    parser.add_argument("--seed", type=int, default=20261018)
    parser.add_argument("--only", type=int, nargs="*", choices=tuple(SLUGS))
    parser.add_argument("--label", default=None)
    args = parser.parse_args()
    label = args.label or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + (
        "-smoke" if args.quick else "-full")
    selected = [index] if index is not None else (args.only or sorted(SLUGS))
    for exp in selected:
        print(f"[EXP-{exp:03d}] mode={'quick' if args.quick else 'full'} "
              f"seed={args.seed} label={label}",flush=True)
        output = run_experiment(exp,seed=args.seed,quick=args.quick,label=label)
        print(f"  saved {output['rows']} metric rows to {SLUGS[exp]}",flush=True)


if __name__ == "__main__":
    main()
