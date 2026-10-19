# EXP-011 — Componentwise kNN Isomap versus other Isomap methods, PCA and t-SNE/UMAP

> **New local run status:** The native EXP-011 Python code is now committed under `proximity_isomap/code/`. The numbers and derived SVG currently shown below are **previous exploratory pilot summaries**, NOT the result of your upcoming Windows run. After you push the new run's CSV/JSON/NPZ and PNG/SVG files, the assistant will replace this preliminary narrative with a mathematical interpretation grounded in your measured outputs. You do not need to download/import any ZIP.

**Research status:** one exploratory local run completed, seed 20261018. The mathematical comparison and selected measured values are on GitHub. The exact original runner, full metrics, embeddings and five original 3D/2D image galleries plus diagnostic plots are still in the local EXP-011 archive pending binary import. UMAP was **not executed**: no missing result has been fabricated.

## Research question

Does separating graph components *before* performing independent Isomap improve intracomponent distance fidelity and prevent projected overlap relative to global Isomap, PCA, t-SNE and UMAP?

Datasets are five separate circles, a connected cylinder, two rotated Swiss rolls, two S-curves and a torus. All fitted methods use the same ambient coordinates and a 2D target. Componentwise methods for some synthetic pairs are given the number of components K, unlike the global baselines: this is an information advantage and not a fair fully automatic comparison.

## Methods actually compared

PCA; global kNN Isomap (k=8,24); global radius Isomap; landmark Isomap; componentwise radius Isomap; componentwise kNN Isomap; componentwise landmark Isomap; t-SNE. **Genuine UMAP is configured but its runtime dependency was unavailable.** Global Isomap may reconnect disconnected neighbor graphs by inserting bridges; the original metrics store those warnings. M-Isomap, D-C Isomap and S-Isomap++ are prior-art targets, not algorithms implemented in this experiment.

## Mathematics: distortion metrics

For analytic within-component intrinsic distances g_ij, use

$$
S_{\mathrm{within}}(Y)=\left(
\frac{\sum_k\sum_{i<j\in C_k}(\|y_i-y_j\|_2-g_{ij})^2}
{\sum_k\sum_{i<j\in C_k}g_{ij}^2}
\right)^{1/2}.
$$

For original and projected component centroids μ^X_k, μ^Y_k, report

$$
S_{\mathrm{centroid}}(Y)=\left(
\frac{\sum_{k<\ell}(\|\mu^Y_k-\mu^Y_\ell\|_2-\|\mu^X_k-\mu^X_\ell\|_2)^2}
{\sum_{k<\ell}\|\mu^X_k-\mu^X_\ell\|_2^2}
\right)^{1/2}.
$$

The original experiment also measures original-ambient trustworthiness (k=8), cross-component ambient stress, intersecting convex-hull pairs, warnings and runtime. Since t-SNE/UMAP target local neighborhoods, ranking them only by geodesic stress is inadequate.

## Selected numerical results

Normalized within-component intrinsic stress, **one sample per geometry; lower is better**:

| Method | Five rings | Cylinder | Two Swiss rolls | Two S-curves |
|---|---:|---:|---:|---:|
| PCA | 0.463 | 0.328 | 0.720 | 0.372 |
| Global Isomap k=8 | 0.460 | 0.272 | 0.733 | 0.355 |
| Global Isomap k=24 | 0.250 | **0.271** | 0.774 | 0.435 |
| **Componentwise radius Isomap** | **0.245** | **0.271** | **0.676** | 0.333 |
| **Componentwise kNN Isomap** | **0.245** | 0.272 | 0.729 | **0.312** |
| t-SNE | 0.354 | 0.381 | 0.721 | 0.342 |
| UMAP | Not run | Not run | Not run | Not run |

On five rings, global Isomap k=24 scored 0.250 intrinsic stress but its ten pairs of projected convex hulls all overlapped. Componentwise Isomap scored approximately 0.245 with **zero hull intersections** but had worse centroid placement (stress ≈2.311) than PCA (≈0.414). This is the motivation for a separation-constrained *centroid/landmark alignment* objective. On rotated Swiss rolls componentwise Isomap can still have high intrinsic stress (~0.676), demonstrating an important negative result. Cylinder t-SNE trustworthiness was ~0.997 despite relatively poor intrinsic stress (~0.381).

![Comparison summary from the measured local run](../../figures/011-isomap_baselines/summary.svg)

## Original figures and full numerical evidence

The original archive holds five 3D/2D embedding galleries (rings, cylinder, Swiss pair, S-curve pair and torus), an intrinsic stress figure, original-ambient trustworthiness, centroid stress plots, the actual method runner and a complete metrics.csv, metadata.json, saved NPZ embeddings and SHA256 manifest. These belong under:

- proximity_isomap/code/011-isomap_baselines/run.py
- proximity_isomap/results/011-isomap_baselines/runs/exploratory_seed20261018/
- proximity_isomap/figures/011-isomap_baselines/runs/exploratory_seed20261018/
- tests/test_exp_011.py

**The new user-run evidence is pending** scripts/run_exp_010_011.ps1. After this script imports the exact ZIP, it replaces this provisional summary note with the original complete note containing all corresponding real PNG image links.

## Scientific limitations

Results use one exploratory seed, untuned hyperparameters and some supplied-K settings; no robust comparative superiority or newness is claimed. Multi-manifold prior art must be verified and implemented. A later independent-seed experiment should install real UMAP and optimize centroid/landmark placement with a positive separation margin.

## Native execution and analysis handoff

The user runs [the committed Python source](../../code/011-isomap_baselines/run.py) using `scripts/run_exp_010_011.ps1 -RequireUmap` after installing `umap-learn`. The assistant reviews the **actual pushed run**, including failed methods, and writes a new interpretation and Marp update. The numbers above are **earlier exploratory pilot measurements**; metric definitions and fresh numbers can differ and must not be silently combined.

## Figure plan and reproduction status

| Expected PNG/SVG plot name | Content | Status |
|---|---|---|
| `rings_embeddings` | Five rings, all baselines | New run pending |
| `cylinder_embeddings` | Cylinder, all baselines | New run pending |
| `swiss_pair_embeddings` | Two rotated Swiss rolls | New run pending |
| `s_curve_pair_embeddings` | Two S-curves | New run pending |
| `torus_embeddings` | Torus | New run pending |
| `intrinsic_stress` | Distance preservation | New run pending |
| `centroid_stress` | Intercomponent positioning | New run pending |
| `trustworthiness_8` | Neighbor structure | New run pending |

Do not embed these new plots before their corresponding files exist on the user's pushed GitHub run.
