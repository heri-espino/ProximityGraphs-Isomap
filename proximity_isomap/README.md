# Experiment research archive — one synchronized home

This is the **canonical experiment-facing research layout**:

```text
proximity_isomap/
  notes/    001-radius_filtration/README.md ... 008-multiple_swiss_rolls/README.md
  code/     001-radius_filtration/ ... 008-multiple_swiss_rolls/
  figures/  001-radius_filtration/ ... 008-multiple_swiss_rolls/
  results/  001-radius_filtration/ ... 008-multiple_swiss_rolls/
```

Each experiment has a stable 3-digit slug shared by the four directories. See [the eight-experiment index](notes/README.md) and [asset availability manifest](MANIFEST.json).

**What belongs where:** notes contain *motivation, what was attempted, observations, interpretation, limitations and relative figure/result links*; code contains the exact runner/config and plot source; results contain numerical metrics and provenance; figures contain actual graphics with captions/source information. Keeping notes and journal identical would lose chronology: `journal/` is an **append-only decision log**, while `proximity_isomap/notes/` is the canonical edited-by-experiment record. The `paper/` folder is a short synthesis, not a duplicated experiment.

**Important provenance:** 001 code and five-point smoke metrics are present on GitHub; the full experimental implementation, PNG/SVG projections and raw outputs for 002–008 were produced in past ChatGPT ZIP archives but **were never imported into this GitHub repository**. This reorganization consolidates the reliably transcribed findings and generates explicitly labeled *summary diagrams*, but **does not pretend those historical projection figures or exact code have been restored**. Check each `code/<id>/README.md` and `results/<id>/README.md` for the precise inventory.

The Python library remains at `src/proximity_isomap/` (needed for editable installation); the root `proximity_isomap/` here is the research archive, *not* a new importable Python package. Scripts in `scripts/`, documentation in `docs/`, source literature in `literature/`, and tests in `tests/` remain at root.

To complete missing historical assets, import the original 260-file research integration bundle into a clean checkout **with a conflict-aware importer**, then map each archived file into the experiment slug and record SHA-256/commit provenance. Never fabricate datasets, saved embeddings, or sample-level statistics.
