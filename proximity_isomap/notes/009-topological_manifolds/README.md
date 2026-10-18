# EXP-009 — Swiss roll, cylinder and torus: do holes survive Isomap?

**Status:** Executed exploratory pilot, 2026-10-18; no statistical validation or novelty claim. The full local original pilot figures/arrays are supplied as a downloadable ZIP in the associated ChatGPT conversation. This repository includes the rerunnable source and a compact summary visualization; regenerated official PNG/SVG figures use the pinned **ContrastColors** library.

## Central question

Can independent Isomap embeddings maintain different homology types while guaranteeing that three graph components remain separated? Real Swiss-roll strips have beta1=0, open cylinders beta1=1, and torus surfaces beta1=2. Graph cycles are not automatically H1 features because VR triangles fill 3-cycles.

## Design

- 54 regular-grid Swiss-roll observations, 54 regular-grid cylinder observations and 64 regular-grid torus observations: 172 points.
- The true **number** of groups K=3 is supplied to the MST-cut algorithm; point labels are withheld during splitting. This does not constitute unsupervised K estimation.
- Each component is independently embedded using an r-neighborhood graph at its own MST connectivity threshold, graph shortest paths and 2D classical MDS.
- Rigid rotations/translations arrange the three 2D embeddings with a 0.9 horizontal minimum gap. Such alignment preserves distances **within the computed embeddings**, not the true intrinsic geometry of the original surfaces.
- H1 VR persistence uses all vertices, edges and triangles, reduced over F2 for original **ambient Euclidean** distances and separately for projected 2D Euclidean distances. The filtration is truncated at r=7, so infinite reported bars are right-censored; lifetime >=1 is an illustrative threshold.

## Measured pilot results

| Manifold | True beta1 | Original sampled H1 bars with lifetime >=1 | After Isomap |
| --- | ---: | ---: | ---: |
| Swiss roll | 0 | 1 | 0 |
| Cylinder | 1 | 1 | 0 |
| Torus | 2 | 9 | 1 |

The torus has excess apparent H1 classes due to finite regular-grid geometry/sampling and the chosen metric, not additional true holes. The Swiss roll also produces a false-positive persistent loop. On the other hand, the cylinder's long H1 bar disappears in the 2D Isomap embedding. **Good component separation does not imply topology preservation.**

Graph split: K=3 correctly recovered given K, with maximum retained MST edge approximately 3.1857 and minimum discarded bridge 14.0228. Rigid separation margin 0.9; internal pair distances changed at most ~5.33e-15. The independent and aligned embedding VR H1 diagrams agree to numerical precision.

## Visual evidence

![EXP-009 pilot: principal persistent H1 lifetimes and components](../../figures/009-topological_manifolds/summary.svg)

Regenerate actual **3D/2D comparison PNG and SVG** and **H1 barcode PNG and SVG** with:

~~~powershell
conda activate proximity-isomap
python proximity_isomap/code/009-topological_manifolds/run.py --output proximity_isomap/results/009-topological_manifolds/runs/pilot
~~~

The output directory is immutable and refuses overwrite. The [versioned GitHub workflow](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/workflows/publish-exp009.yml) has already generated and committed the official ContrastColors PNG/SVG images and NPZ/JSON results below. The original local pilot package is also available as a downloadable research ZIP.


## Mathematics: persistent holes and topology across embeddings

The Vietoris–Rips complex at distance threshold \(r\) consists of simplices whose **every pair** of vertices lies at distance at most \(r\):

$$
\operatorname{VR}_r(X)=
\bigl\{\sigma\subseteq X:
\max_{x_i,x_j\in\sigma}\|x_i-x_j\|_2\le r\bigr\}.
$$

Its connected-component count is \(\beta_0(r)=\dim H_0(\operatorname{VR}_r)\); \(\beta_1(r)=\dim H_1(\operatorname{VR}_r)\) counts independent unfilled 1-cycles. Graph triangles are filled by 2-simplices and therefore do not necessarily create \(H_1\) holes.

For the ideal supports used here,

$$
\begin{array}{c|ccc}
\text{Support}&\beta_0&\beta_1&\beta_2\\ \hline
\text{Swiss-roll strip}&1&0&0\\
\text{Cylinder (open)}&1&1&0\\
\text{Torus surface}&1&2&1
\end{array}
$$

These are *support* Betti numbers, **not** guaranteed VR counts for finite samples or every radius. An \(H_1\) persistence class is recorded by its birth and death scales \((b,d)\); its lifetime is \(d-b\), subject to truncation at the maximum filtration radius. Our lifetime threshold \(d-b\ge 1\) is descriptive, not a formal significance test.

Crucially, for each independent Isomap embedding \(Z_k\) and its rigidly aligned version \(Y_k=Z_kQ_k+t_k\),

$$
\|z_i-z_j\|_2=\|y_i-y_j\|_2
\quad\Longrightarrow\quad
\operatorname{Dgm}_p(\operatorname{VR}(Z_k))
=\operatorname{Dgm}_p(\operatorname{VR}(Y_k)).
$$

But in general \(\operatorname{Dgm}_p(\operatorname{VR}(X_k))\ne
\operatorname{Dgm}_p(\operatorname{VR}(Z_k))\): graph-geodesic Isomap does **not** preserve original ambient Euclidean VR persistence automatically.

**Interpretation:** the cylinder's loss of a prominent \(H_1\) bar is a failure of this *independent embedding stage*, not of its later rigid placement. Different filtrations or sample densities may yield different results; plot barcodes and projection geometry side by side.

## Figure plan and reproduction status

**Already generated:** the final section of this note embeds the actual `geometry.png` and `h1_barcodes.png` files from the versioned EXP-009 pilot. Subsequent independent-seed experiments remain pending.

| Planned output filename | Mathematical point to illustrate | Current status |
|---|---|---|
| `geometry.png` | 3D original, global PCA, and separated Isomap | Generated in versioned EXP-009 run |
| `h1_barcodes.png` | H1 persistence for original ambient and independent 2D embeddings | Generated in versioned EXP-009 run |

**After a new run:** confirm that image filenames and actual metric fields match the notes before interpreting the figures. [Plot directory](../../figures/009-topological_manifolds/README.md) · [Result directory](../../results/009-topological_manifolds/README.md).

## Interpretation

The failure of topology preservation is a real research concern, but neither proof of a universally defective embedding nor a novel observation by itself. Equalities concern VR diagrams on independent Z_k vs rigidly transformed Y_k; they do **not** establish preservation of the original X_k diagrams. Compare with TopoMap/TopoMap++ and DIPOLE, tune sampling and radius, use several independent binomial/Poisson realizations, and establish a non-oracle unsupervised K/r selector before seeking publication.

<!-- GITHUB-GENERATED-EXP009: latest original figures -->

## Generated EXP-009 figures and frozen results

This is a fresh versioned rerun using the pinned ContrastColors library,
not an image reconstructed from the rounded summary. Run: \`run_d8aff3bb97\`.

![Original 3D, PCA and componentwise Isomap projections](../../figures/009-topological_manifolds/runs/run_d8aff3bb97/geometry.png)

![Measured H1 persistence before/after Isomap](../../figures/009-topological_manifolds/runs/run_d8aff3bb97/h1_barcodes.png)

Full [persistence pairs and metadata](../../results/009-topological_manifolds/runs/run_d8aff3bb97/metrics.json) and
[observation/embedding arrays](../../results/009-topological_manifolds/runs/run_d8aff3bb97/coordinates.npz). Both figure
panels are also saved as SVG in the matching numbered figures directory.
