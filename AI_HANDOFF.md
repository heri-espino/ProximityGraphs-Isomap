# AI handoff — current research session

**Last updated:** 2026-10-18
**Latest journal entry:** [2026-10-18 — Numbered experiment archive consolidation](journal/2026-10/2026-10-18-experiment-archive-consolidation.md)
**Project stage:** exploratory scaffold with an agreed working paper thesis; novelty not established

> This is the **current operational snapshot**, not a substitute for the chronological journal or primary evidence. Start with [`journal/README.md`](journal/README.md), [`journal/LATEST.md`](journal/LATEST.md), and its linked entry **before** reading this file.

## 2026-10-18 — Canonical numbered research archive (CURRENT)

**Start at [proximity_isomap/notes/README.md](proximity_isomap/notes/README.md) for EXP-001 through EXP-008**, with synchronized slug folders for `code/`, `figures/`, and `results/`. Each experiment note explains the attempted method, metrics, observations, negative results and actual figure links. Journal entries are chronology; experiment notes are the maintained synthesis.

[Availability manifest](proximity_isomap/MANIFEST.json) is explicit: exact original source and original smoke measurements are present for 001 only. EXP-002–008 rounded historical metrics have been archived as *transcriptions* and their SVG charts are redraws—not original 3D/2D projections. **The missing 260-file historical archive still needs import** (see `scripts/restore_experiment_archive.py`). No new geometric experiment was executed in this reorganization. Do not report missing numerical outputs as recovered.

**Immediate next:** obtain/verify the historical ZIP, restore exact experiment source and original figures without overwriting CI/environment/paper content, update manifest to reflect recovered assets, then rerun from a versioned Git SHA. The requested scientific direction remains the separation–distortion frontier in `paper/RESEARCH_DIRECTION.md`.

## Archived numerical evidence (2026-10-17)

Representative numeric results from EXP-0004/7/8 and the progression across EXP-0002–0008 are now accessible in [results/EXPLORATORY_OVERVIEW.md](results/EXPLORATORY_OVERVIEW.md). They are source-transcribed exploratory summaries, **not yet regenerated from GitHub main**. Latest journal: [2026-10-17 — Archived numerical summaries](journal/2026-10/2026-10-17-archived-numerical-summaries.md). Full binary figures, CSV/NPZ, code and test imports still require the local bundle and Git push.

## Dependency preparation for pending archive import (2026-10-17)

**Latest journal:** [2026-10-17 — Prepare experiment dependencies](journal/2026-10/2026-10-17-exp-dependencies.md). The repo now defines the optional `experiments` dependency group for scikit-learn and Matplotlib, and CI installs this group. This prepares for the EXP-0002–0008 archive but **does not mean the binary results are on GitHub**.

## 2026-10-17 — Pending full results import (current operational status)

**Latest journal:** [2026-10-17 — Prepared experiment history integration](journal/2026-10/2026-10-17-archive-integration-prepared.md).

The EXP-0002–0008 archives have been reconciled into a tested *local* import bundle (260 source/data/figure files, 57 tests passing, all file hashes verified). This bundle is **not yet on GitHub main** because this connection cannot upload binary PNG/NPZ archive files directly. The complete ZIP and importer were delivered in this chat. Do not claim their GitHub integration is complete. Run the importer against a clean clone, confirm the push and the CI job, then run representative scientific experiments again under a recorded Git SHA. The working manuscript thesis in `paper/RESEARCH_DIRECTION.md` remains authoritative. See [status index](experiments/ARCHIVE_INTEGRATION_STATUS.md).

## 2026-10-17 — Current working paper direction

Read [paper/RESEARCH_DIRECTION.md](paper/RESEARCH_DIRECTION.md) **before drafting the manuscript**. The central question is how much cross-component placement fidelity must be sacrificed to preserve the geometry of independently embedded components and guarantee non-overlap. Four linked aims: (1) unsupervised proximity-graph components; (2) independent Isomap/geodesic preservation; (3) rigid alignment with positive hull clearance; (4) a normalized separation–distortion frontier. The paper outline is revised in paper/main.tex. ADR-0005 documents the choice; elementary proofs are in notes/results/PROP-0002-rigid-separation-frontier.md.

**Crucial evidence boundary:** EXP-0002–EXP-0008 were run in local ZIP research archives and discussed in chat, **not yet merged into or reproduced from GitHub main**. The main branch still lacks their optimized alignment implementation. Do not quote their statistics as versioned publication results. The current branch's last verified CI relates to the earlier 16-test scaffold. The 2026-10-17 paper/thesis changes passed GitHub Actions run [39086961855](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/39086961855) on Python 3.11 and 3.12 (pytest, Ruff, integrity validation, Sphinx). LaTeX compilation and Conda solving were not part of that run. No experimental data from local ZIPs was validated.

**Immediate scientific priority:** verified multi-manifold novelty review, then integrate exploratory code with the remote CI state; establish an unsupervised radius and compare frontiers to strong baselines. Do not claim separation alone is new.

## Scientific objective

Investigate whether radius and other proximity graphs can support manifold dimensionality reduction with disconnected components. Two candidates are (1) normalized hybrid stress minimization and (2) independently embedded components with rigid alignment. The advantages, novelty and robustness remain to be established.

## Verified / implemented

- A pairwise-distance `r`-neighborhood builder and connected-component labels: `src/proximity_isomap/graphs/radius.py`.
- Hybrid finite dissimilarity evaluation and normalized within/between stress **evaluation**, not minimization: `src/proximity_isomap/distances/hybrid.py`, `src/proximity_isomap/embedding/stress.py`.
- A minimal synthetic Swiss-roll radius-sweep script: `experiments/EXP-0001.md`. It is exploratory, not evidence of superiority.
- A package, Sphinx configuration, tests, Obsidian-compatible notes, journal, paper outline, and research-literature workflow.

## Not verified / not implemented

- Hybrid MDS optimizer, componentwise rigid alignment optimizer, tuned Isomap and Euclidean MDS benchmarks.
- Any new theorem, convergence rate, original algorithm, or comparative performance claim.
- The `literature/` pipeline has templates and a catalog but **no imported primary-source PDFs or reviewed paper summaries yet**. The pre-existing Isomap BibTeX metadata is not a review.

## Decisions still active

- Use `||x_i-x_j|| <= r` rather than overlap of two radius-`r` balls: `ADR-0002`.
- Retain both candidate embedding objectives pending benchmarks: `ADR-0003`.
- Read the chronological journal first, then update a session handoff and literature records: `ADR-0004`.

## Conda environment and initial run

- The root `environment.yml` now specifies Python 3.11, conda-forge packages (including testing, Sphinx and benchmarking), and an editable package install. See `docs/getting-started.md`.
- EXP-0001 executed in a **plain Python sandbox from an extracted starter ZIP**, not from a Conda environment or a checked-out Git repository. All 16 tests passed and the script generated five rows. At r=7 its within-component RMSE was 26.2789938496, compared with 1.2395593716 at r=5. **This is not a controlled causal result.** The evaluated pairs differ at smaller disconnected radii; Git SHA was unavailable.
- Conda solving, Ruff, Sphinx and checked-out-revision experiments remain **unverified** here.

## Immediate next actions

0. Create the Conda environment, rerun tests/Ruff/Sphinx and EXP-0001 from a versioned Git checkout, and archive run/environment metadata.

1. Import a small set of baseline papers with PDFs, Docling Markdown, and annotated result records. Confirm any claimed theorems against the original PDF.
2. Implement baseline embeddings before proposing a new optimizer; benchmark under identical datasets and frozen evaluation criteria.
3. Update this handoff, `journal/LATEST.md`, the latest journal entry, and the context summaries after **each substantive repository-editing session**.

## CI status

- GitHub Actions on the Conda-preparation commit installed the editable package and ran **16/16 passing tests**, but Ruff failed on four auto-fixable diagnostics: one UP017 datetime alias and three I001 import-block spacing issues.
- Follow-up commit `e7cc9bcf723e72ebec7ec0d133f03d117020b56d` passed GitHub Actions run [38997728144](https://github.com/heri-espino/ProximityGraphs-Isomap/actions/runs/38997728144) on Python **3.11 and 3.12**, including tests (16), Ruff, research validation, and a warnings-as-errors Sphinx build. This is **pip-based CI**, not a tested Conda solve.

## Most recent checks

- `PYTHONPATH=src python -m pytest -q`: **16 passed**. `python scripts/validate_research.py`: **PASS**. `compileall` for src/tests/scripts: **PASS**.
- **Ruff and Sphinx were not run locally:** missing dependencies; an attempted `pip install -e ".[dev,docs]"` was blocked by unavailable network/package-index access. CI remains configured to run them. See the dated journal for detail.

## Handoff checklist

- [ ] Read latest journal and relevant primary evidence first.
- [ ] Document proofs versus conjectures and experiment evidence precisely.
- [ ] Maintain NumPy-style Sphinx-compatible docstrings for public APIs.
- [ ] Record new literature sources in the manifest and per-paper result notes.
- [ ] Run relevant checks, noting failures and skipped checks.
- [ ] Append the journal entry and update `journal/LATEST.md`.
- [ ] Refresh this handoff and the `context/` snapshot.
