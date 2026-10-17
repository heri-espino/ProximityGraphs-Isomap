# Manuscript

This is an intentionally minimal LaTeX skeleton, **not a submission-ready draft**. No novelty or empirical result has yet been validated. `main.tex` compiles a preliminary outline.

The **single canonical BibTeX database** lives in [`../literature/references/library.bib`](../literature/references/library.bib), not in this folder. Every cited mathematical result should have a source-checked annotation under `literature/references/` and ideally an entry in `KEY_RESULTS.md`.

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

When adding results, cite experiment IDs/commit SHAs in source comments or supplementary notes. Store selected camera-ready figures in `../figures/paper/`.
