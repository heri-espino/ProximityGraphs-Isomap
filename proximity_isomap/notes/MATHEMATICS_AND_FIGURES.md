
# Mathematical notes and experiment-figure conventions

**For all EXP-001 through EXP-009.** The nine experiment notes are the canonical reader-facing explanations. Reusable mathematical results and assumptions can be derived in [mathematics/](mathematics/index.md); do not copy the same proof into every experiment.

## Write the mathematics alongside intuition

Each experiment note should have:

1. **Question and geometric intuition.** Explain what the sampling and embedding are meant to demonstrate.
2. **Mathematics.** Define symbols, input distances, graph rule, objective, constraints and what exactly is preserved.
3. **Method and provenance.** Clarify sample count, radius selection, solver/seed, baselines and source revision.
4. **Findings and negative results.** A result may be a failure; differentiate measured values from predictions or untested hypotheses.
5. **Figures.** Display *existing* images using relative Markdown references and give each one an explanatory caption.

Use GitHub/Obsidian-compatible inline math (\`$...\`) and display math (\`$$...$$\`), without screenshotting equations. For a new note:

~~~markdown
## Mathematics: objective

Let $X=\{x_1,\dots,x_n\}\subset\mathbb R^D$. Define

$$
E(Y)=\sum_{i<j}(\|y_i-y_j\|_2-d_{ij})^2.
$$

Explain how $d_{ij}$ is constructed and whether it is a known analytic
geodesic, an estimated graph distance, or an ambient Euclidean distance.
~~~

In particular, **the graph radius is an edge threshold** \`||x_i-x_j|| <= r\`, not a ball-overlap threshold. Distinguish true geometric components (synthetic evaluation labels) from automatically detected graph components. A rigid pose preserves **computed** intracomponent distances, not necessarily the true geodesic distances. Infinite cross-manifold intrinsic paths are not the same thing as finite ambient cross distances.

## Figure-link policy

**Existing figure:**

~~~markdown
![EXP-NNN — what is shown and why it matters](../../figures/NNN-short_title/runs/RUN_ID/figure.png)
~~~

The markdown relative path must exist **at commit time**. Link the corresponding SVG where helpful; do not embed a nonexistent file to reserve space. Before a new run, list expected filenames and captions in the experiment's **Figure plan and reproduction status** table instead.

**When a full experiment is executed:**

- Use \`contrastcolors\` with the pinned \`heri\` style and Okabe–Ito palette from \`environment.yml\`.
- Save real \`.png\` and \`.svg\` outputs under \`proximity_isomap/figures/NNN-short_title/runs/RUN_ID/\`.
- Save CSV metrics, JSON metadata, NPZ coordinates and source SHA/checksums under the matching \`results/NNN-short_title/runs/RUN_ID/\`.
- Append a **Computed run: RUN_ID** section with figure images, observed metrics and interpretations, keeping all earlier run reports in the note. A run should not silently erase a previous experiment record.
- Include negative findings, uncertain interpretations, and caveats (oracle radius, fixed K, solver local minima).
- Validate with \`python scripts/validate_experiment_archive.py\`, pytest, Ruff, Sphinx and inspect the actual images before pushing.

## Figure provenance

- **EXP-001–008 historical \`summary.svg\`**: reconstructed plots from rounded reported historical aggregates, *not* original 3D/2D panels.
- **EXP-001–008 full new PNG/SVG**: pending user local \`./scripts/run_all.ps1 -Push\`.
- **EXP-009**: genuine 3D/2D and \(H_1\) barcode PNG/SVG exist and are embedded in [its experiment note](009-topological_manifolds/README.md).
- Do not mix newly reconstructed experiments with historical implementations when making scientific claims; the old integration ZIP is explicitly excluded.
