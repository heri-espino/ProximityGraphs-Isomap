"""Experiment 005 runnable wrapper for newly reconstructed experiments."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_runner import main  # noqa: E402


if __name__ == "__main__":
    main(5)
