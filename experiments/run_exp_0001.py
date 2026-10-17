"""EXP-0001 exploratory Swiss-roll radius sweep (no embedding optimization)."""

import argparse
import csv
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import scipy
from scipy.sparse.csgraph import shortest_path
from scipy.spatial.distance import pdist, squareform

from proximity_isomap import radius_graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/exp_0001/smoke"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if config["experiment_id"] != "EXP-0001":
        raise ValueError("Unexpected experiment ID")
    if args.output.exists():
        raise FileExistsError(f"Output path already exists: {args.output}")

    rng = np.random.default_rng(config["seed"])
    n = int(config["n_points"])
    if n < 2:
        raise ValueError("At least 2 points are required")
    t = rng.uniform(config["t_min"], config["t_max"], size=n)
    h = rng.uniform(config["height_min"], config["height_max"], size=n)
    x = np.column_stack((t * np.cos(t), h, t * np.sin(t)))
    u = 0.5 * (t * np.sqrt(1.0 + t * t) + np.arcsinh(t))
    intrinsic = squareform(pdist(np.column_stack((u, h))))

    rows = []
    tri = np.triu_indices(n, k=1)
    for radius in config["radii"]:
        graph = radius_graph(x, float(radius))
        within = graph.component_labels[tri[0]] == graph.component_labels[tri[1]]
        graph_dist = shortest_path(graph.adjacency, directed=False)
        predicted = graph_dist[tri][within]
        truth = intrinsic[tri][within]
        error = float(np.sqrt(np.mean(np.square(predicted - truth)))) if len(truth) else None
        rows.append({
            "radius": float(radius),
            "n_components": graph.n_components,
            "n_edges": graph.n_edges,
            "n_within_pairs": int(within.sum()),
            "n_between_pairs": int((~within).sum()),
            "within_graph_vs_intrinsic_rmse": error,
        })

    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        git_sha = None

    metadata = {
        "experiment_id": config["experiment_id"],
        "run_at_utc": datetime.now(UTC).isoformat(),
        "source_config": str(args.config),
        "config": config,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "git_sha": git_sha,
        "disclaimer": "Exploratory descriptive sweep; varying evaluated pair sets.",
    }
    args.output.mkdir(parents=True, exist_ok=False)
    with (args.output / "metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (args.output / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
