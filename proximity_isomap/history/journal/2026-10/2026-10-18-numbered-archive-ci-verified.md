# 2026-10-18 — Verified the numbered experiment archive on GitHub

**Scope:** GitHub structural verification only; no EXP-002–008 scientific rerun.

## Successful CI verification

- Final GitHub Actions run: https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39134370194.
- Checked out commit `0303a9f9d883964aa83fc7742d4f1bd4de0d21a4` after resolving intermediate Ruff and Sphinx formatting failures.
- The final matrix completed successfully, including Python tests, Ruff, existing research-integrity validation, the new numbered-archive/link validator, and Sphinx builds. The earlier two interim red CI runs were fixed rather than ignored.
- All eight notes, code/recovery inventories, figures and result inventories are present and their note links resolve.
- EXP-001 original script, config and smoke data are copied byte-for-byte; historical EXP-002–008 raw code/binary plot assets remain **absent** from GitHub main.

## What success does and does not mean

The archive reorganization is now **committed and structurally verified**. Successful CI is not a proof of newly published geometry or reproduced experimental performance. The reconstructed SVG summary plots are not 3D source projections. The historical ZIP import still needs its SHA-256 provenance and full simulation reruns under Git.

## Next task

Recover the original `ProximityGraphs-Isomap-Research-History-Integration.zip` generated in the earlier session, inspect/dry-run `scripts/restore_experiment_archive.py`, apply safe missing-file moves and verify all source+binary hashes. Then update per-experiment provenance/readme statuses and repeat numerical experiments under a recorded Git SHA.
