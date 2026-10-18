# EXP-0001–EXP-0008 — Research progression and integration status

**Current GitHub status (2026-10-17):** EXP-0002–EXP-0008 source, CSV/NPZ and full figures remain in a tested local archive; **not yet present on `main`**. Read [integration preparation journal](../journal/2026-10/2026-10-17-archive-integration-prepared.md). The scientific data will become available here only after the import package is committed and pushed.

| Experiment | Topic | Main observation |
| --- | --- | --- |
| EXP-0001 | Radius graph baseline | Pair sets differ under fragmentation; conditional errors are not directly comparable |
| EXP-0002 | Hybrid MDS baseline | Naive Euclidean intercomponent distances can distort manifold geodesics |
| EXP-0003 | Radius sweep | Very narrow low-stress regimes and abrupt shortcut changes |
| EXP-0004 | Transfer across density/manifold | A global radius may fail under density shift |
| EXP-0005 | Two Swiss rolls and two S-curves | Within-manifold intrinsic stress and between-manifold ambient stress conflict |
| EXP-0006 | Rotated Swiss rolls | PCA cannot unfold both differently oriented nonlinear surfaces |
| EXP-0007 | Separating two components | Rigid alignment preserves computed internal distances but affects relative placement |
| EXP-0008 | One through six rolls | K-component positive-gap alignment; pilot label-informed radius, limited seeds |

**Critical distinction:** true intrinsic geodesic distances between disconnected generating manifolds are infinite; cross-manifold stress targets ambient Euclidean distances. The local experiments used imperfect and not fully tuned baselines, sometimes one-start nonlinear optimization, and true component labels to choose diagnostic radii. Do not represent these as a finished publishable benchmark.

**Import protocol:** Download the research integration archive from the original ChatGPT conversation; use its `README_IMPORT.md` and `import_into_repo.py` against a current clean Git checkout. The import adds an updated `experiments/EXPERIMENT_INDEX.md` and `results/PROVENANCE_EXP0002_EXP0008.json` with 260 content hashes.
