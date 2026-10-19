# Professor presentation checkpoint — Marp

[Open presentation.md](presentation.md) to read the full lecture deck as Markdown. The file contains 63 Marp slides, including the central mathematical development, versioned experimental results and an atlas of 21 published-run PNGs plus 9 historical SVG summaries.

This **is not** a new numerical experiment. The checkpoint is deliberately located in notes/010_presentation_checkpoint, as requested. It does not replace either the existing 009 topology work or the local EXP-010/011 numerical experiment folders.

## Export on Windows with PowerShell

From the repository root, with Node.js and a supported local browser installed:

~~~powershell
npx --yes @marp-team/marp-cli@latest proximity_isomap/notes/010_presentation_checkpoint/presentation.md --allow-local-files --pdf -o presentation_checkpoint.pdf
npx --yes @marp-team/marp-cli@latest proximity_isomap/notes/010_presentation_checkpoint/presentation.md --allow-local-files --pptx -o presentation_checkpoint.pptx
~~~

All versioned figures use relative paths into proximity_isomap/figures and are verified to exist on GitHub main. The deck also includes provisional **text-only** discussion of EXP-010 (radius/density: cylinder versus rings) and EXP-011 (Isomap baselines, t-SNE, UMAP). Their local PNGs/SVGs have not been integrated into this repository; they must be versioned and the deck updated before presenting them as repository figures. No broken figure links have been introduced.

## Research evidence

- Experimental index: [../README.md](../README.md)
- Working paper: [../../../paper/RESEARCH_DIRECTION.md](../../../paper/RESEARCH_DIRECTION.md)
- EXP-009: [../009-topological_manifolds/README.md](../009-topological_manifolds/README.md)
- TDA and stochastic geometry notes: [../mathematics/research_tda_stochastic_geometry.md](../mathematics/research_tda_stochastic_geometry.md)

The main slides end with the literature list; the remaining pages are optional image-atlas backup slides. Distinguish computed within-embedding distances from synthetic ground truth, and between-manifold ambient distances from nonexistent cross-manifold intrinsic geodesics.
