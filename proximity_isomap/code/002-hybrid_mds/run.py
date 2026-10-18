"""Experiment 002 runnable wrapper for newly reconstructed experiments."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_runner import main  # noqa: E402, I001


if __name__ == "__main__":
    main(2)
