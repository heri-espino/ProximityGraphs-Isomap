# EXP-009 pilot code

[run.py](run.py) is a standalone fully deterministic Swiss-roll/cylinder/torus point-cloud generator with K=3 MST component cutting, independent Isomap and exact small-sample VR H1 persistence reduction. Install the repository Conda environment (includes pinned ContrastColors), then run:

```powershell
python proximity_isomap/code/009-topological_manifolds/run.py --output proximity_isomap/results/009-topological_manifolds/runs/pilot_new
```

All JSON/NPZ and actual PNG/SVG files are written to the new output directory; this does not rerun EXP-001–008. Complete scientific interpretation is in the [note](../../notes/009-topological_manifolds/README.md).
