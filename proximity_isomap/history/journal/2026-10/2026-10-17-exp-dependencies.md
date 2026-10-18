# 2026-10-17 — Prepare experiment dependencies for archive integration

**Status:** Packaging and CI dependency preparation, not integration of experiment data.

The pending EXP-0002–0008 import includes scikit-learn-based PCA/Isomap and Matplotlib figure generation. The original package depended only on NumPy and SciPy. Added an `experiments` optional extra containing `scikit-learn>=1.4,<2` and `matplotlib>=3.8,<4`, and updated GitHub Actions to install `.[dev,docs,experiments]`.

The Conda environment already includes the benchmarking and plotting libraries and was preserved. The new archival ZIP uses the current repository checkout for dependencies and must not overwrite `pyproject.toml` or CI files.

**Scientific status:** The 260 files containing EXP-0002–0008 code, metrics, arrays, figures, and original journals have been reconciled and passed a simulated import, but they **are not present on GitHub main yet**. See [the prior integration preparation record](2026-10-17-archive-integration-prepared.md). Verification of this dependency change will occur in its GitHub Actions run; full scientific reproduction still requires the subsequent import and separate reruns.
