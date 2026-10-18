"""EXP-009 pilot: Isomap vs original H1 persistence for Swiss roll/cylinder/torus.

This is a new deterministic pilot, not the proposed full EXP-009 benchmark.
It uses known K=3 (but not labels) when cutting the Euclidean MST.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree, shortest_path
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA


def generate() -> tuple[np.ndarray, np.ndarray]:
    """Generate three deterministic grid samples from topologically distinct supports.

    Returns
    -------
    tuple of ndarray
        Ambient coordinates (172,3) and generating labels (172,). The label
        array is for evaluation only and is not used in graph construction.
    """
    t, h = np.meshgrid(np.linspace(1.6*np.pi, 4.35*np.pi, 9),
                       np.linspace(-5, 5, 6), indexing="ij")
    swiss = np.column_stack((.35*t.ravel()*np.cos(t.ravel()),
                             .5*h.ravel(), .35*t.ravel()*np.sin(t.ravel())))
    a, z = np.meshgrid(np.arange(9)*2*np.pi/9, np.linspace(-4, 4, 6), indexing="ij")
    cylinder = np.column_stack((3.1*np.cos(a.ravel()), 3.1*np.sin(a.ravel()),
                                z.ravel()))
    a, b = np.meshgrid(np.arange(8)*2*np.pi/8, np.arange(8)*2*np.pi/8, indexing="ij")
    torus = np.column_stack(((5+1.85*np.cos(b.ravel()))*np.cos(a.ravel()),
                              (5+1.85*np.cos(b.ravel()))*np.sin(a.ravel()),
                               1.85*np.sin(b.ravel())))
    blocks = [swiss, cylinder, torus]
    for i in (1, 2):
        blocks[i][:, 0] += blocks[i-1][:, 0].max()+14-blocks[i][:, 0].min()
    return np.vstack(blocks), np.repeat(np.arange(3), (54, 54, 64))


def cut_mst(x: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Cut two longest MST edges, supplying K=3 but not generating labels.

    Parameters
    ----------
    x : ndarray
        Ambient observations.

    Returns
    -------
    tuple
        Ordered component identifiers and the largest remaining and shortest
        removed MST edge weights.
    """
    tree = minimum_spanning_tree(squareform(pdist(x))).tocoo()
    order = np.argsort(tree.data)
    keep = order[:-2]
    i, j = tree.row[keep], tree.col[keep]
    weights = tree.data[keep]
    g = csr_matrix((np.r_[weights, weights], (np.r_[i, j], np.r_[j, i])),
                   shape=(len(x), len(x)))
    count, labels = connected_components(g, directed=False)
    if count != 3:
        raise RuntimeError(f"Expected three graph components, got {count}")
    ordered = sorted(np.unique(labels), key=lambda q: x[labels == q, 0].mean())
    mapped = np.array([ordered.index(q) for q in labels])
    return mapped, float(tree.data[order[-3]]), float(tree.data[order[-2]])


def classical_mds(d: np.ndarray) -> np.ndarray:
    """Classical 2D MDS from a complete finite dissimilarity matrix.

    Parameters
    ----------
    d : ndarray
        Symmetric pairwise target distances.

    Returns
    -------
    ndarray
        Two-dimensional coordinates.
    """
    a = d*d
    gram = -.5*(a-a.mean(axis=0)[None, :]-a.mean(axis=1)[:, None]+a.mean())
    values, vectors = np.linalg.eigh(gram)
    return vectors[:, -2:]*np.sqrt(np.maximum(values[-2:], 0))


def embed_components(x: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Fit independent Isomap and make disjoint rigid x-strips with margin 0.9.

    Parameters
    ----------
    x : ndarray
        Ambient observations.
    labels : ndarray
        Unsupervised MST component labels with K supplied.

    Returns
    -------
    tuple
        Independent 2D coordinates and separated 2D coordinates.
    """
    independent = np.zeros((len(x), 2))
    aligned = np.zeros_like(independent)
    lastmax = None
    for k in range(3):
        mask = labels == k
        block = x[mask]
        d = squareform(pdist(block))
        tree = minimum_spanning_tree(d)
        r = float(tree.data.max()*(1+1e-9))
        paths = shortest_path(csr_matrix(np.where((d > 0) & (d <= r), d, 0)),
                              directed=False)
        if not np.isfinite(paths).all():
            raise RuntimeError("Internal radius graph is disconnected")
        z = classical_mds(paths)
        independent[mask] = z
        z = z-z.mean(axis=0)
        if np.ptp(z[:, 0]) > np.ptp(z[:, 1]):
            z = z @ np.array([[0, 1], [-1, 0]])
        if lastmax is not None:
            z[:, 0] += lastmax+0.9-z[:, 0].min()
        aligned[mask] = z
        lastmax = float(z[:, 0].max())
    return independent, aligned


def h1_rips(x: np.ndarray, rmax: float = 7) -> list[tuple[float, float]]:
    """Compute exact H1 bars over F2 using vertices, edges, filled triangles.

    Parameters
    ----------
    x : ndarray
        Metric point cloud for the Euclidean Vietoris--Rips filtration.
    rmax : float
        Maximum VR edge threshold; surviving bars are right-censored.

    Returns
    -------
    list[tuple[float,float]]
        Finite or right-censored (infinite) birth/death values for H1.
        This small-n reference implementation is not a Ripser replacement.
    """
    d = squareform(pdist(x))
    n = len(x)
    cells = [(0.0, 0, (i,)) for i in range(n)]
    cells.extend((float(d[i, j]), 1, (i, j)) for i in range(n)
                 for j in range(i+1, n) if d[i, j] <= rmax)
    for i, j, k in itertools.combinations(range(n), 3):
        radius = max(d[i, j], d[i, k], d[j, k])
        if radius <= rmax:
            cells.append((float(radius), 2, (i, j, k)))
    cells.sort(key=lambda e: (round(e[0], 11), e[1], e[2]))
    index = {c[2]: i for i, c in enumerate(cells)}
    pivots: dict[int, set[int]] = {}
    born = set()
    bars: dict[int, list[tuple[float, float]]] = defaultdict(list)
    for idx, (radius, dim, vertices) in enumerate(cells):
        col = set() if dim == 0 else {
            index[tuple(face)] for face in itertools.combinations(vertices, dim)
        }
        while col and max(col) in pivots:
            col ^= pivots[max(col)]
        if not col:
            born.add(idx)
        else:
            p = max(col)
            pivots[p] = col
            birth, lowdim, _ = cells[p]
            if lowdim == 1 and radius-birth > 1e-9:
                bars[1].append((birth, radius))
            born.discard(p)
    bars[1].extend((cells[i][0], float("inf")) for i in born if cells[i][1] == 1)
    return sorted(bars[1], key=lambda bar: (-(bar[1]-bar[0]), bar[0]))


def main() -> None:
    """Compute pilot measurements and figures with pinned ContrastColors."""
    import contrastcolors as cc

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    folder = args.output
    if folder.exists():
        raise FileExistsError("Refusing to overwrite original EXP-009 run")
    folder.mkdir(parents=True)
    cc.set_style("heri", palette="okabe-ito", font="DejaVu Sans", use_tex=False)
    colors = list(cc.color_palette("okabe-ito", as_hex=True))
    x, truth = generate()
    labels, bottleneck, bridge = cut_mst(x)
    independent, separated = embed_components(x, labels)
    if not np.array_equal(labels, truth):
        raise RuntimeError("Pilot failed supplied-K partition check")
    names = ("Swiss roll", "Cylinder", "Torus")
    summary = []
    hist = {}
    for k, name in enumerate(names):
        mask = labels == k
        before = h1_rips(x[mask])
        after = h1_rips(independent[mask])
        rigid = h1_rips(separated[mask])
        if len(after) != len(rigid):
            raise RuntimeError("Rigid alignment changed H1 bar count")
        hist[name] = {"original": before, "isomap": after}
        summary.append({
            "manifold": name, "n": int(mask.sum()),
            "h1_original_lifetime_ge_1": sum(d-b >= 1 for b, d in before),
            "h1_isomap_lifetime_ge_1": sum(d-b >= 1 for b, d in after),
            "rigid_distance_change_max": float(
                np.max(np.abs(pdist(independent[mask])-pdist(separated[mask])))
            ),
        })
    np.savez_compressed(folder/"coordinates.npz", x=x, truth=truth, labels=labels,
                        independent=independent, separated=separated)
    (folder/"metrics.json").write_text(
        json.dumps({"K_supplied": 3, "partition_accuracy": 1.0,
                    "sampled_internal_mst_bottleneck": bottleneck,
                    "sampled_bridge_min": bridge, "rips_truncation": 7,
                    "summary": summary, "h1_bars": hist}, indent=2)
    )
    fig = plt.figure(figsize=(15, 5), layout="constrained")
    axes = [fig.add_subplot(1, 3, 1, projection="3d"),
            fig.add_subplot(1, 3, 2), fig.add_subplot(1, 3, 3)]
    pca = PCA(n_components=2).fit_transform(x)
    for k in range(3):
        ids = labels == k
        axes[0].scatter(*x[ids].T, s=12, color=colors[k])
        axes[1].scatter(*pca[ids].T, s=12, color=colors[k])
        axes[2].scatter(*separated[ids].T, s=12, color=colors[k])
    axes[0].view_init(elev=19, azim=-64)
    for ax, title in zip(axes, ("Original 3D", "Global PCA",
                               "Independent Isomap + separation"), strict=True):
        ax.set_title(title, fontsize=11)
    for ax in axes[1:]:
        ax.set_aspect("equal", adjustable="datalim")
    for ext in ("png", "svg"):
        fig.savefig(folder/f"geometry.{ext}", dpi=175)
    plt.close(fig)
    fig, axes = plt.subplots(3, 2, figsize=(11, 9), layout="constrained", sharex=True)
    for k, name in enumerate(names):
        for j, key in enumerate(("original", "isomap")):
            ax = axes[k, j]
            for q, (birth, death) in enumerate(hist[name][key][:11]):
                ax.plot([birth, min(death, 7)], [q, q], color=colors[k], lw=3.1)
            ax.set_xlim(0, 7.1)
            ax.set_ylim(-0.6, 11.1)
            ax.set_yticks([])
            ax.set_title(f"{name}: {key}")
            ax.grid(axis="x", alpha=.13)
    for ext in ("png", "svg"):
        fig.savefig(folder/f"h1_barcodes.{ext}", dpi=175)
    plt.close(fig)
    print(json.dumps({"K": 3, "n": len(x), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
