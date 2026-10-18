# 2026-10-17 — Index verified archived numerical summaries

**Status:** Summary tables imported as text from the original local EXP-0002–0008 CSV archives. Full experimental binaries/code are still pending local Git import.

## Action

Added `results/EXPLORATORY_OVERVIEW.md` recording EXP-0004, EXP-0007 and EXP-0008 representative numerical comparisons and the principal conclusions and limitations across EXP-0002–0008. Values were transcribed from the archived CSV snapshots and rounded for readability. This makes core experimental observations available directly on GitHub while the full file and plotting archive is awaiting a versioned push.

## Evidence limits

Historical exploratory source execution passed 57 tests locally and all 260 file hashes passed in a simulated checkout. Those checks did not rerun the archived experiments or establish original Git source identities. In particular, EXP-0008 used an oracle (true-component-based) radius; the within-surface metric is intrinsic stress while cross-surface stress uses ambient Euclidean distances. No scientific novelty or generality is asserted.

## Next steps

Complete the binary-and-source import package, push, verify GitHub Actions, and rerun selected experiments under recorded commit SHA, then conduct a primary-source novelty review and held-out comparison.
