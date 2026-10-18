# Manuscript workspace

**Current stage:** Research thesis and preliminary LaTeX outline, not a submission-ready paper. Novelty and comparative performance remain unverified.

**Start here:** [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md) is the canonical working contribution: *preserve separately unfolded manifold geometry while optimizing a controlled separation–distortion tradeoff*. It specifies definitions, objectives, elementary guarantees, candidate evidence and falsification criteria. The central scientific question is how much global geometric fidelity is sacrificed to keep independent components separate.

## Working manuscript

- [main.tex](main.tex): compact manuscript outline; sections under [sections/](sections/). Statements must not present the proposed contribution as validated.
- [PROP-0002](../notes/results/PROP-0002-rigid-separation-frontier.md): proofs of basic rigid invariance, sufficient strip separation and frontier monotonicity. These elementary properties are not yet novel results.
- [Research journal](../journal/README.md), [AI handoff](../AI_HANDOFF.md): source of project decisions and present status.
- [Literature workflow](../literature/README.md): PDF originals, Docling Markdown and source-checked mathematical results. The sole canonical bibliography is [library.bib](../literature/references/library.bib).
- [Results](../results/) and [figures](../figures/): only cite experimental findings after the exact code, configuration, independent seed results and Git revision are integrated and verified.

### Compile the outline (if LaTeX is installed)

    cd paper
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

No publication venue, title, main contribution or theorem priority is finalized. Aim for a short (~5–7 page) main text only if the results support a defensible method claim.

## Experiment evidence map

The manuscript's experimental explanations and provenance are maintained in [proximity_isomap/notes/](../proximity_isomap/notes/README.md), with matching code/results/figure slugs. The SVGs are reconstructed historical summaries, not the original projection panels. Raw plots and source from EXP-002–008 still require import before citing them as fully reproducible evidence.
