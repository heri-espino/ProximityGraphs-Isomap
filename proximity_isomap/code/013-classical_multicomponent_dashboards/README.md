# EXP-013 executable — classical far/near 3x3 dashboards

The native Python source is [run.py](run.py). The experiment code is committed and awaits the user's Windows execution.

## Reproduce with PowerShell

Run from the repository root:

~~~powershell
git pull --ff-only
conda activate proximity-isomap
conda install -n proximity-isomap -c conda-forge umap-learn -y
python -m pytest tests/test_exp013_classical_dashboards.py -q
.\scripts\run_exp_013.ps1 -Quick
.\scripts\run_exp_013.ps1 -RequireUmap -Push
~~~

The quick run is for smoke testing only. The full run with -Push saves and publishes a new immutable UTC-labeled result/figure directory. To generate without publishing, omit -Push and commit/push only the new full-run results and figure folders afterward.

The full default covers 7 families × far/near = 14 cases. Two 3×3 dashboards per case are generated (28 total), with 12 distinct methods in their union. Each case also has an original 3D source diagram and a k-detection versus k-embedding diagnostic, all as PNG and SVG.

The runner saves method_metrics.csv, detected_components_vs_k.csv, knn_detection_embedding_grid.csv, scenario_metadata.csv, raw/embedded NPZ files, metadata.json and SHA256 checksums. Failures are recorded without synthetic substitutes.

**Research integrity:** the true labels only inform evaluation, plotting, and the explicitly named oracle-K baseline. Near/far source separation is verified. The torus intrinsic geodesic metric is unavailable and is recorded as missing.

[Mathematical pre-run note](../../notes/013-classical_multicomponent_dashboards/README.md). After the user's full run is pushed, the assistant will examine the data and add all 28 real dashboards to the [shared lecture](../../notes/012-presentation_checkpoint/componentwise_knn_isomap_lecture.md).