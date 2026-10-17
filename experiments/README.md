# Experiment registry and reproducibility contract

Each experiment has a **stable ID** `EXP-####`, a human-readable protocol, a version-controlled JSON configuration, and a runnable script.

| ID | Question | Protocol | Script | Status |
| --- | --- | --- | --- | --- |
| EXP-0001 | How do components and graph-geodesic error change with the radius on a known synthetic manifold? | [Protocol](EXP-0001.md) | `run_exp_0001.py` | Implemented, not evaluated as research |

## Rules

- Record the data-generation process and random seed, actual software versions, timestamp, and Git SHA when available.
- Never tune hyperparameters on the same intrinsic-distance ground truth later used for scientific evaluation. A future benchmark will require development and test splits (or repeated independently seeded manifolds).
- Report disconnected structure explicitly: number and size of components, number of finite graph-distance pairs and cross-component pairs.
- Keep **within graph-geodesic stress**, **between ambient-distance stress**, and **true intrinsic-distance error** conceptually distinct.
- Do not overwrite previous run output without choosing a new `--output` path; generated run IDs should be immutable once referenced in the manuscript.
- Commit compact summaries/metrics when validated. Do not commit large point clouds, intermediate matrices or cached arrays.

First smoke run:

```bash
python experiments/run_exp_0001.py --config experiments/configs/exp_0001.json --output results/exp_0001/smoke
```
