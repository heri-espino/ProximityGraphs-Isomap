# Literature review and provenance

The canonical literature corpus is `literature/README.md`. For each paper, keep its original PDF in `pdf/`, Docling-derived Markdown in `markdown/`, and a **source-verified** result note in `references/` under one shared citation key.

Maintain `MANIFEST.csv` and the cross-paper `references/KEY_RESULTS.md` index. Every mathematical result should include its source PDF page, printed theorem/equation identifier, assumptions, proof idea, verification state, and comparison to our research hypotheses. No extraction tool guarantees correct mathematics.

Use the standard-library scaffolder:

```bash
python scripts/new_literature_entry.py --key author2024topic --title "Article title" --year 2024
```

Then ingest and verify the source according to `literature/README.md`. The manuscript reads the sole BibTeX database at `literature/references/library.bib`.
