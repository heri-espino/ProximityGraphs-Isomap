# Working hypothesis — Vietoris–Rips + random geometric graphs + separation-constrained Isomap

**2026-10-18 | Status:** Research direction, not a validated improved model.
**Reproduction tasks:** See [NEXT_STEPS](../../history/context/NEXT_STEPS.md).
**Elementary deterministic result:** [PROP-0003](results/PROP-0003-component-recovery-window.md).

## Motivation

Rather than simply rendering K non-overlapping Swiss rolls, ask whether **0-dimensional persistent homology plus stochastic geometry** can support an *unsupervised radius choice* and *quantitative probability of correct component recovery*, before independent geodesic Isomap and rigid placement.

Original pipeline (candidate):

    random sample X from separated manifold supports S_1,...,S_K
      -> proximity graph filtration r ↦ G_r = 1-skeleton(VR_r(X))
      -> infer a stable component partition / choose r from H_0 + sampling assumptions
      -> independent Isomap within graph components
      -> rigid poses with positive projected clearance
      -> study the separation–ambient-distortion frontier V(μ)

Do **not** conflate (a) β0/persistence recovery, (b) geodesic-distance consistency, and (c) correct placement in the plane. They are different claims.

## Structural bridge: 0-dimensional persistence and the Euclidean MST

The n−1 finite H0 merge/death radii of the VR filtration equal the sorted edge lengths accepted by Kruskal's MST algorithm (ties counted). Therefore all radius graph component transitions can be computed efficiently without evaluating full high-dimensional simplicial homology. Define β0(r) as number of connected components at radius r. A plateau with β0(r)=K is a **candidate** stable partition, not proof K is correct.

For synthetic known groups, define b=max_k bottleneck(MST(X_k)) and δ=min cross-group sampled distance. [PROP-0003](results/PROP-0003-component-recovery-window.md) proves exact recovery iff b≤r<δ, with Γ=δ−b>0. Label information may be used only as a diagnostic in experiments, never to tune a purported unsupervised method.

## Random sampling hypotheses and elementary high-probability bound

Assume compact connected supports S_k embedded in R^D, separated by a strictly positive ambient gap Δ = min_{k≠l}dist(S_k,S_l)>0. Choose r<Δ. For each support, choose finitely many open Euclidean balls B(c_{kj},r/4) centered on S_k that cover S_k. Let M_k be their number and let p_{kj} be the probability mass of each ball under a distribution P_k with support S_k (assume p_{kj}>0).

- **Binomial point process:** independently sample n_k points on S_k from P_k, condition on fixed counts. Probability ball j is empty is (1−p_{kj})^{n_k} ≤ exp(−n_k p_{kj}).
- **Poisson point process on S_k:** with finite intensity measure Λ_k, probability ball j contains no point is exp(−Λ_k(B(c_{kj},r/4))). For a lower intensity λ_k p_{kj} it is bounded by exp(−λ_k p_{kj}).

If every cover ball contains at least one sample, then G_r restricted to S_k is connected: the intersection graph of the relative open cover of connected S_k is connected; representatives from two overlapping r/4 balls are at distance <r, and each sample lies within <r of a representative. Since r<Δ, no inter-support edge is possible. By a union bound,

    Pr(correct components | n_1,...,n_K)
      ≥ 1 − Σ_k Σ_{j=1}^{M_k} exp(−n_k p_{kj})

for independent per-support binomial samples, and

    Pr(correct components)
      ≥ 1 − Σ_k Σ_{j=1}^{M_k} exp(−Λ_k(B(c_{kj},r/4)))

for independent support-wise Poisson processes, unconditionally (provided this bound is meaningful). These are **elementary coverings/void-probability bounds** under strong assumptions, not a new probability theorem.

Under d-dimensional regularity (covering M_k(r) ≤ C_k r^(−d) and ball masses ≥ c_k r^d for sufficiently small r), the binomial failure upper bound scales at most like

    Σ_k C_k r^(−d) exp(−c_k n_k r^d).

This motivates the familiar connectivity scale r ≍ (log n_k / n_k)^(1/d) and illustrates why finite density can make the correct-radius interval disappear. This is **not** a sharp threshold statement for general curved manifolds or nonuniform densities. For actual intrinsic-manifold PPP, specify intensity relative to intrinsic d-dimensional volume/Hausdorff measure, not an ambient D-dimensional Poisson process conditioned on a measure-zero support.

The above only concerns graph components. To prove Isomap's geodesic accuracy, one also needs control of manifold curvature/reach, shortcut edges and sampling coverage. If the support gap Δ=0 (touching/intersecting manifolds) the deterministic argument does not apply.

## Comparison methods — source-verified candidate baseline families

| Work | Relevance | Caveat |
| --- | --- | --- |
| M-Isomap (Fan, Qiao, Zhang, 2009) | Multi-manifold geodesics and intermanifold constraints | Compare implementation/pipeline fairly |
| S-Isomap++ (Mahapatra, Chandola, 2017) | Multiple/intersecting manifolds, streaming | Streaming assumption differs |
| MMD-Isomap (Yang, Xiang, Zhang, 2016) | Explicit within-geometry and cross-class separation | **Supervised**, using class labels; oracle upper-bound baseline, not equivalent unsupervised input |
| TopoMap (Doraiswamy et al., 2020) and TopoMap++ (2024/25) | Guarantees **full H0 VR diagram** preservation | Strongest direct challenge to any claim of new H0-preservation guarantee |
| DIPOLE (Wagner, Solomon, Bendich, 2021) | Isomap/metric geometry plus persistence objective | Topological-plus-metric synthesis already exists |
| Joint MDS (Chen et al., ICLR 2023) | Unsupervised manifold alignment | Operates on multiple datasets; objective/input may differ |
| Ordinary PCA, tuned single/manifold Isomap | Fair standard references | Handle disconnected shortest paths explicitly |

### Primary pointers (verify PDF and exact algorithms before implementation)

- Fan et al. *Isometric Multi-Manifolds Learning*, https://arxiv.org/abs/0912.0572
- Mahapatra & Chandola, *S-Isomap++*, https://arxiv.org/abs/1710.06462
- Yang et al., *Multi-manifold Discriminant Isomap*, https://doi.org/10.1016/j.patcog.2016.02.001
- Doraiswamy et al., *TopoMap*, https://doi.org/10.1109/TVCG.2020.3030441
- Guardieiro et al., *TopoMap++*, https://doi.org/10.1109/TVCG.2024.3456365
- Wagner et al., *Improving Metric Dimensionality Reduction with Distributed Topology*, https://arxiv.org/abs/2106.07613
- Chen et al., *Unsupervised Manifold Alignment with Joint MDS*, https://openreview.net/pdf?id=lUpjsrKItz4
- Penrose, *Random Geometric Graphs*, Oxford University Press (2003), https://doi.org/10.1093/acprof:oso/9780198506263.001.0001
- Penrose, Yang, Higgs, *Largest nearest-neighbour link and connectivity threshold*, https://doi.org/10.1007/s41468-023-00154-5
- Bobrowski & Kahle, *Topology of random geometric complexes: a survey*, https://doi.org/10.1007/s41468-017-0010-0
- Turner (2019), Rips persistence stability, https://doi.org/10.2140/agt.2019.19.1135

## Next *new* experiment and falsifiable hypotheses

**Reserve EXP-009** for comparing multi-manifold Isomap / TopoMap against persistence-informed radius selection plus constrained alignment. Do not mark EXP-009 executed.

1. Recompute full EXP-001–008 later with the pinned Conda PowerShell workflow; note differences from historical rounded records.
2. On matched data, vary n_k, K, intrinsic dimension d, ambient manifold gap Δ, curvature/fold distance, sampling density and perturbation ε; use binomial and manifold-supported Poisson point processes.
3. Compute full H0 barcodes from MST edges. Estimate r *without labels*, for example by candidate long plateau(s) combined with density calibration; choose any tuning constants on training/development data only.
4. Report true component recovery **only for evaluation**, false merges/splits, β0 persistence discrepancies after projection, within true geodesic stress, cross ambient stress, achieved hull clearance, runtime, and seed-level confidence intervals.
5. Compare same graph and same partition for embedding subproblem *and* compare fully automatic end-to-end baselines, marking any supervised/oracle baseline clearly.
6. Test negative cases: crossing manifolds (Δ=0), very unequal n_k, sparse folds, noise and outliers. If a global threshold cannot separate them (Γ≤0), report impossibility rather than selecting labels.
7. Decide whether the mathematical contribution is a *new probabilistic result*, a *new radius-calibration algorithm*, or a *new practical constrained-embedding frontier*. Existing MST, RGG and TopoMap results are not novelty by themselves.

**Publication discipline:** a 5–7-page paper requires one central defensible improvement and a few decisive figures. These ideas are a candidate extension, not several simultaneously established contributions.

## Candidate extension: H1 holes, H2 cavities and their visualization

**Status (2026-10-18):** Proposed diagnostic, not a completed EXP-009 benchmark.

The graph G_r is the 1-skeleton of VR_r(X) under the distance-threshold convention. Graph cycles are **not** the same as H1 classes: a triangle whose three edges exist is filled by a VR 2-simplex, making its boundary null-homologous. Compute persistent H1 in the simplicial complex, not the graph cycle rank.

| Ideal support | beta0 | beta1 | beta2 |
| --- | ---: | ---: | ---: |
| Swiss roll or S-curve strip | 1 | 0 | 0 |
| Two separate strips | 2 | 0 | 0 |
| Circle / annulus / cylindrical surface | 1 | 1 | 0 |
| Two separate circles | 2 | 2 | 0 |
| Torus surface | 1 | 2 | 1 |
| Hollow sphere surface | 1 | 0 | 1 |

These are topological Betti numbers of ideal supports, not guarantees for finite-sample VR at every radius. Noise and uneven sampling may produce short-lived spurious classes.

**Illustrative calculation (not an experiment report):** an elementary finite VR boundary reduction over F2 on two separated regular unit circles with 18 points each produced two long H1 intervals (birth,death) approximately (0.347296, 1.732051). Two H0 classes persisted over the radius range considered. A preview figure was generated in chat, not committed as an original ContrastColors experiment panel.

**Important rigid invariance:** For independent Isomap coordinates Z_k and rigidly aligned coordinates Y_k=Z_k Q_k+t_k, the complete within-component pairwise Euclidean distance matrix remains equal. Therefore the full within-component VR filtrations and all their persistence diagrams are identical between Z_k and Y_k. This is elementary and not a novelty theorem. However the VR diagrams of the original ambient X_k versus independent Isomap Z_k can differ substantially; Isomap aims to approximate geodesic targets rather than ambient Euclidean distances. Global VR persistence may also change even if every within-component VR diagram is fixed.

A uniform maximum absolute error <= epsilon for all corresponding pairwise distances gives epsilon-shifted inclusions of VR complexes in both directions, providing a stability route for persistent homology. Ordinary normalized root stress alone does not provide a maximum-error guarantee.

**Proposed visualizations (later EXP-009 diagnostic):** actual VR point-cloud/graph/triangle panels at increasing radii; H0/H1 barcode or diagram; representative loop overlay on the source geometry; paired diagrams of the original data, independent Isomap, and rigidly separated alignment. Use pinned contrastcolors for all generated PNG/SVG and embed them with their metrics into the numbered notes. Ripser.py can compute H0/H1 and output *cohomological cocycles*; those are not automatically geometric homology-cycle representatives. GUDHI is an alternative for simplicial complexes and H2.

**Critical negative controls:** Swiss rolls/S-curves have no true H1, while annuli/cylinders and tori do. Include noise, outliers, sparse rings, unequal densities, and intersecting manifolds to study false positives.

**References:** [GUDHI VR guide](https://gudhi.inria.fr/python/latest/rips_complex_user.html), [Ripser.py API](https://ripser.scikit-tda.org/en/latest/reference/stubs/ripser.ripser.html), [Ripser representative cocycles](https://ripser.scikit-tda.org/en/latest/notebooks/Representative%20Cocycles.html), and [TopoMap H0 preservation](https://www.ime.unicamp.br/~pjssilva/papers/topomap/). These are source pointers, not a completed prior-art novelty matrix.
