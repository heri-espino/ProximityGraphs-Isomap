# Research workflow and AI handoff

## Ordered start-of-session reading

1. `journal/README.md`, `journal/LATEST.md`, and its linked date-stamped entry.
2. `AI_HANDOFF.md`, the short, current summary.
3. `context/STATE.md`, `context/NEXT_STEPS.md`, and relevant decisions.
4. Only task-relevant mathematics, source code, experiments and primary literature.

`AGENTS.md` is the entrypoint prescribing this procedure. If the summary conflicts with an original paper, tested implementation or dated decision, examine and document the conflict.

## Finish every substantive research-editing session

Update source and tests; run appropriate checks; append an immutable dated journal entry with rationale, changed files, tested commands, failures and open questions; update the latest pointer, handoff and current context. Record literature changes in the manifest and annotated source results, and experimental runs in their original configurations.

## Sphinx API docstring convention

Public modules, classes and functions require **NumPy-style docstrings**. Parameters, Returns, Raises and Notes are descriptive sections rather than slogans. Record mathematical definitions, edge-weight conventions, shape expectations, units and numerical failure modes. Keep API docs generated directly from source with `sphinx.ext.autodoc` and `sphinx.ext.napoleon`; don't maintain conflicting handwritten copies of function behavior.

For example:

```python

def f(x: float, radius: float) -> bool:
    """Return whether a nonnegative distance lies within the cutoff.

    Parameters
    ----------
    x : float
        Nonnegative Euclidean endpoint distance.
    radius : float
        Positive cutoff in the same units as ``x``.

    Returns
    -------
    bool
        Whether ``x <= radius``.

    Notes
    -----
    The threshold does not test overlap between full radius-``radius`` balls.
    """
    return x <= radius
```

Run `python scripts/validate_research.py` to check the basic structure and `python -m sphinx -b html -W docs docs/_build/html` to check Sphinx itself. These are necessary structural checks, not sufficient scientific verification.


## Experiment-focused research record

Use [the canonical numbered archive](../proximity_isomap/notes/README.md). Update an experiment's one narrative README and the corresponding code/results/figures; add a chronological journal entry only for the new research action or decision. Do not copy an entire journal entry into each experiment note. Run `python scripts/validate_experiment_archive.py` alongside the main validator. The historical EXP-002–008 assets are explicitly marked incomplete until the original ZIP is restored.
