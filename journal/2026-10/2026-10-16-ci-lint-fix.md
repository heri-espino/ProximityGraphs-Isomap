# 2026-10-16 — Ruff CI compatibility fixes

**Status:** source hygiene / CI repair; no change to the graph mathematics or experiment conclusions.

## Trigger

GitHub Actions run 38997593526 for the Conda-environment commit
installed the editable package and **passed all 16 tests**, but stopped
at Ruff linting with four auto-fixable errors:

- UP017: use Python 3.11 `datetime.UTC` rather than `timezone.utc`
  in `experiments/run_exp_0001.py`.
- I001: three extra blank lines in import blocks in
  `scripts/check_change_protocol.py`, `scripts/new_literature_entry.py`
  and `scripts/validate_research.py`.

## Action

Apply exactly those minimal changes, leaving the numerical experiment
and data configurations unchanged. Append this journal entry, move
`journal/LATEST.md`, update the current AI handoff and research state.

## Verification and limitations

Earlier pip-based CI passed 16 tests. Ruff, structural validation and
Sphinx must run again on the follow-up revision; do not claim success
until the new workflow finishes. There is still no local Conda solve.

## Next

Inspect CI outcome and any remaining errors. Run the tracked Conda
environment and EXP-0001 on a machine with Conda, archive package
versions and Git SHA, then proceed to standard MDS/Isomap baselines.
