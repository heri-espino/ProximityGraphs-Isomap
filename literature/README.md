# Literature corpus — source-backed research

This is the **canonical** literature directory. Never store a second annotated literature corpus in `notes/literature/` or duplicate the primary BibTeX database in `paper/`.

## Required structure

```text
literature/
├── MANIFEST.csv               # one row per paper; machine-readable state
├── pdf/                       # original source PDFs; exact filenames by citation key
├── markdown/                  # Docling-extracted Markdown (not authoritative)
└── references/
    ├── library.bib            # single canonical bibliography
    ├── PAPER_TEMPLATE.md      # required per-paper annotation sections
    ├── KEY_RESULTS.md         # cross-paper result locator and synthesis index
    └── <citation_key>.md      # manually checked result summaries
```

## Source authority and naming

Choose a stable ASCII BibTeX citation key (`tenenbaum2000`, `author2024topic`, etc.). It must be unique. Expected paths for a paper are:

- `literature/pdf/<citation_key>.pdf`
- `literature/markdown/<citation_key>.md`
- `literature/references/<citation_key>.md`

`MANIFEST.csv` stores the key, metadata, relative paths, and import/review statuses. Original PDFs provide authoritative statements and equation numbering. Docling Markdown is an indexing and reading aid; **check mathematical symbols, figures, tables, footnotes and theorem boundaries against the PDF**. Record the conversion version and any known extraction errors in the annotation.

## Ingestion workflow

1. Create the catalog and annotation record (without inventing results):

   ```bash
   python scripts/new_literature_entry.py --key author2024topic --title "Article title" --year 2024
   ```

2. Copy the legally obtained PDF to `literature/pdf/author2024topic.pdf`; update the manifest's `extraction_status` to `pdf_only`.
3. Convert it using [Docling's official CLI](https://github.com/docling-project/docling/blob/main/docs/reference/cli.md). With a current Docling release, for example:

   ```bash
   python -m pip install docling
   docling convert literature/pdf/author2024topic.pdf --to md --output literature/markdown
   ```

   CLI options can change across releases: verify using `docling convert --help`. Pin the Docling version in the annotation; set `extraction_status=extracted` **only after** checking that the Markdown exists. Do not overwrite manually corrected Markdown silently.
4. Read the PDF and extracted Markdown; fill in `references/author2024topic.md` using `PAPER_TEMPLATE.md`: assumptions, symbols, theorem/result IDs, statement in your own words, exact source locator, proof technique, limitations, method, comparison with our work, and verification status. Update `review_status=reviewed` only when all claims have been checked against the PDF.
5. Add each **verified** result that matters to our work to `references/KEY_RESULTS.md`, with a link to the per-paper annotation and an exact PDF locator. Add a valid BibTeX record to `references/library.bib`.
6. Run `python scripts/validate_research.py` and record any substantive synthesis or changed hypothesis in the research journal.

## Catalog status values

- `extraction_status`: `pending` (no PDF), `pdf_only` (PDF, no extracted Markdown), `extracted` (PDF and Markdown).
- `review_status`: `unreviewed`, `in_progress`, `reviewed` (verified against the PDF).

Do not copy lengthy copyrighted extracts into summaries. Summarize mathematical statements in your own words, attribute precise source locations, and preserve the primary PDF reference. Don't assert a result merely because an AI or extraction tool generated plausible text.

## The literature-review question

For every paper, explicitly answer: **What was already known, under which assumptions, and what remains open relative to disconnected proximity-graph Isomap and distance-distortion optimization?**
