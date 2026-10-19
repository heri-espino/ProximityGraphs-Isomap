# EXP-013 — Classical multi-manifold dashboards: far versus near

**Status: code committed; user-run results and images are pending.** This is the *pre-run scientific protocol*, not an interpretation of data that have not been generated. [Python implementation](../../code/013-classical_multicomponent_dashboards/run.py) · [Windows launcher](../../../scripts/run_exp_013.ps1).

The shared Marp lecture is a **research notebook**, not a short publicity presentation: it should eventually contain every real 3×3 dashboard, the mathematics, the experimental decisions, failed cases, unresolved doubts, limitations and proposed follow-ups.

## 1. Research question

When independently generated manifolds are **well separated** versus **close but geometrically disjoint**, how does componentwise kNN-Isomap behave relative to standard manifold-learning and dimensionality-reduction methods? What changes when the kNN neighborhood size used for **component detection** differs from the size used for **within-component unfolding**?

### Seven families; 14 scenarios

| Family identifier | Supports | Geometry |
|---|---:|---|
| rings | 3 | Separate circular curves |
| springs | 2 | Classical 3D helical springs |
| swiss_rolls | 2 | Rotated Swiss-roll surfaces |
| s_curves | 2 | Nonlinear S-curve strips |
| planes | 2 | Flat planar patches (easy control) |
| tori | 2 | Torus surfaces (topology-rich control) |
| cylinder_and_ring | 2 | Cylindrical surface versus one circle |

Each family is evaluated in two regimes: **far** and **near**. The same intrinsic samples and rotation seeds are used for both regimes, changing only translations. Consequently changes between regimes can be attributed to relative ambient placement (for this fixed finite sample).

### Precisely defined separation

For each sampled support, compute the distance to its eighth within-support nearest neighbor, then let $\rho$ be the median of those distances over components. Choose the target sampled-point clearance

$$
g_{\rm near}=0.48\rho,\qquad g_{\rm far}=7\rho.
$$

The runner translates consecutive supports into **disjoint first-coordinate bounding intervals** and matches second/third coordinates at their nearest extreme points. Therefore the selected extreme pair is exactly $g$ apart, and no pair across those consecutive supports can have Euclidean distance smaller than $g$. The minimum **sampled** intersupport distance is recorded explicitly in CSV; there is no deliberate intersection.

**Caveat:** this guarantees separation of finite point samples and their first-coordinate bounding intervals. It is not an independently proved clearance bound for continuous manifold supports beyond the samples.

## 2. Two dashboards, both exactly 3×3

### A. Isomap-centered 3×3

| | | |
|---|---|---|
| PCA | Classical MDS | Global kNN Isomap |
| Global radius Isomap | **Componentwise kNN Isomap** | Componentwise radius Isomap |
| MST-cut + kNN Isomap (oracle K) | t-SNE | UMAP |

### B. General dimensionality reduction 3×3

| | | |
|---|---|---|
| PCA | Classical MDS | Spectral embedding |
| LLE | **Componentwise kNN Isomap** | LTSA |
| t-SNE | UMAP | Global kNN Isomap |

There are **12 distinct methods** in the union of both grids, each fit only once per scenario and reused visually. An algorithm that fails or cannot be used on a disconnected graph must be displayed as **NOT AVAILABLE**, preserving the failure in the metrics CSV rather than replacing it with artificial coordinates.

For the **MST-cut + kNN** comparator, the true *number* of supports K is supplied as an **oracle diagnostic**; the truth partition labels are not used to construct that MST cut. Every method apart from this oracle uses the unlabeled point cloud alone. Ground-truth labels are used to color figures and calculate *evaluation-only* partition/metric scores.

## 3. Mathematics: a true kNN-based component detector

For observations $x_i\in\mathbb R^D$, the symmetrized union kNN graph is

$$
G_{k_d}=(V,E_{k_d}),\qquad
\{i,j\}\in E_{k_d}
\iff j\in N_{k_d}(i)\ \text{or}\ i\in N_{k_d}(j).
$$

Its connected components $C_1,\ldots,C_{\widehat K}$ provide the **detected** partition without being told K or the labels. For a fixed dataset with deterministic neighbor ordering,

$$
k_d\le k_d' \implies
E_{k_d}\subseteq E_{k_d'}
\implies \widehat K(k_d')\le \widehat K(k_d).
$$

Inside each detected component we **recompute** a separate symmetrized $k_e$-NN graph. On connected local graphs, shortest-path distances estimate geodesics:

$$
\widehat d_{G_c}(i,j)=
\min_{\pi:i\leadsto j}\sum_{(u,v)\in\pi}\|x_u-x_v\|_2.
$$

Then classical MDS forms

$$
B_c=-\frac12H_cD_c^{\circ 2}H_c,\qquad
H_c=I-\frac1{n_c}\mathbf1\mathbf1^\top,
$$

and takes the leading positive eigenpairs of $B_c$ for a 2D embedding. Detected components are placed rigidly in nonoverlapping **coordinate strips**. If two generating manifolds were mistakenly joined in the *detected graph*, they are embedded as one group and are **not secretly separated using true labels**.

Unlike EXP-011, EXP-013 therefore performs **global kNN detection itself**, without a global radius threshold or supplied-K MST cut for its main method.

## 4. Sweeps and measured quantities

Main dashboards use $k_{\rm detect}=8$, $k_{\rm embed}=10$. Additional sweeps assess

$$
k_{\rm detect}\in\{3,5,8,12,18,26\},\qquad
k_{\rm embed}\in\{6,10,16\}.
$$

The graph sweep records detected component count, adjusted Rand index against synthetic evaluation truth, cross-support graph edges, and within-support fragmentation. The two-dimensional sweep records within-manifold stress, trustworthiness, cross/centroid stress, convex-hull overlaps/clearance, runtime and failures for each pair of neighborhood sizes.

To compare methods with arbitrary embedding scale, the **evaluation** uses the common positive scale

$$
s(Y)=\sqrt{
\frac{\sum_c\sum_{i<j\in C_c}\|x_i-x_j\|_2^2}
{\sum_c\sum_{i<j\in C_c}\|y_i-y_j\|_2^2}},
\qquad \widetilde Y=s(Y)Y.
$$

True generating component labels here are used **for evaluation only**. Analytic geodesics $g_{ij}$ are available for rings, springs, cylinders and parametrized flat intrinsic strips/sheets:

$$
S_{\rm within}=
\sqrt{\frac{\sum_c\sum_{i<j\in C_c}
(\|\tilde y_i-\tilde y_j\|_2-g_{ij})^2}
{\sum_c\sum_{i<j\in C_c}g_{ij}^2}}.
$$

For the torus, the implementation does not compute an exact intrinsic surface geodesic and marks the corresponding metric **N/A** rather than inserting an ambient approximation as ground truth. Intercomponent *intrinsic* geodesics are not finite for disconnected supports; use original ambient cross-distances for the separate placement metric:

$$
S_{\rm between}=
\sqrt{\frac{\sum_{c<\ell}\sum_{i\in C_c,j\in C_\ell}
(\|\tilde y_i-\tilde y_j\|_2-\|x_i-x_j\|_2)^2}
{\sum_{c<\ell}\sum_{i\in C_c,j\in C_\ell}\|x_i-x_j\|_2^2}}.
$$

Additional measures: local trustworthiness, centroid stress, convex-hull intersections and sampled projected hull gap, method runtimes and saved warnings/errors. These assess different goals; **no single metric establishes superiority**. The simple strip layout is a feasible placement heuristic, *not* the optimizer of the proposed separation–distortion frontier.

## 5. Expected outputs and figure plan

For each of the fourteen scenarios, generate four **actual PNG/SVG figure pairs**:

| Stem | Actual content | Status |
|---|---|---|
| source_3d | Source manifold sample in 3D | Waiting for user run |
| dashboard_isomap_centered | 3×3 Isomap-family comparison | Waiting for user run |
| dashboard_general_dimred | 3×3 general-method comparison | Waiting for user run |
| k_detection_and_embedding | Component counts and detection/unfolding-k stress grid | Waiting for user run |

**Total planned:** 28 dashboards, 14 original source plots, 14 k-diagnostic figures; hence **56 PNGs and 56 SVGs** for a full run, plus data and tables. Do not embed ungenerated image paths in this note or the Marp lecture.

The source script also saves method_metrics.csv, detected_components_vs_k.csv, knn_detection_embedding_grid.csv, scenario_metadata.csv, the original input/embedding NPZ arrays, metadata.json and sha256.json under an immutable UTC run ID in the matching results/figures folders.

## 6. Hypotheses and things we do not know yet

**Predictions, not measured findings:** small detection-k may fragment sparsely sampled manifolds; large detection-k can create cross-manifold bridges when supports are near; componentwise unfoldings preserve computed internal geometry but can sacrifice ambient centroid arrangement; t-SNE/UMAP may achieve high trustworthiness without preserving global placement.

**Open questions:** Does a nonempty usable k interval exist for every family? Does near/far alter the k interval predictably? Are the source supports topologically disjoint but their projected convex hulls overlapping? Does componentwise separation degrade trustworthiness? What happens to the intrinsic errors on helices versus Swiss-roll surfaces? When do LLE, LTSA or ordinary Isomap fail?

The study uses one seed by default; robust inference requires further independent runs. After execution we will record **failed fits, surprising results, limitations and unresolved theoretical questions**, not only successful dashboards.

## 7. Run, publish, and interpret

From a clean Windows Git checkout, run the launcher [scripts/run_exp_013.ps1](../../../scripts/run_exp_013.ps1) with Quick, then the full option RequireUmap, and push the true run outputs. The assistant will then **read the actual saved CSV, source arrays and figures**, add measured analysis and genuine figure links to this note, expand the class lecture [componentwise kNN-Isomap](../012-presentation_checkpoint/componentwise_knn_isomap_lecture.md) with all 28 dashboards, and update AGENTS/handoff/journal.

**No result or figure has yet been generated for EXP-013.**
