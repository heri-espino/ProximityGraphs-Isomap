"""Create honest SVG visualizations from archived summary CSV (not original runs).

This regenerates a *descriptive chart* and must not be used to claim that the
original observations, Isomap embeddings, or simulation code were recovered.
"""

from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path


def render_summary(
    source: Path, output: Path, *, x: str, y: str, title: str,
) -> None:
    """Draw a simple line chart from a numeric summary CSV.

    Parameters
    ----------
    source : Path
        Historical summary CSV with header column names `x` and `y`.
    output : Path
        Output `.svg` pathname; its parent directory must exist.
    x : str
        CSV column used for x labels in original row order.
    y : str
        Numeric CSV column to visualize.
    title : str
        Human-readable chart title.

    Returns
    -------
    None
        Writes a labeled SVG summarizing existing numeric data.

    Raises
    ------
    ValueError
        When source values are missing, nonnumeric or not plottable.
    """
    with source.open(newline="", encoding="utf-8") as stream:
        records = list(csv.DictReader(stream))
    if not records:
        raise ValueError("Summary CSV has no observations")
    try:
        labels = [escape(record[x]) for record in records]
        values = [float(record[y]) for record in records]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Required x/y data are absent or nonnumeric") from exc
    import math

    if not all(math.isfinite(v) for v in values):
        raise ValueError("Nonfinite summary values cannot be plotted")
    ymax = max(1e-9, max(values) * 1.12)
    width, height = 920, 455
    left, right, top, bottom = 100, 35, 70, 108
    iw, ih = width - left - right, height - top - bottom
    pts = [
        (left + i * iw / max(1, len(values) - 1), top + ih * (1 - v / ymax))
        for i, v in enumerate(values)
    ]
    path = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{left}" y="38" font-size="21" font-family="Arial">{escape(title)}</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+ih}" stroke="#444"/>',
        f'<line x1="{left}" y1="{top+ih}" x2="{width-right}" y2="{top+ih}" stroke="#444"/>',
        f'<polyline points="{path}" fill="none" stroke="#0072B2" stroke-width="3"/>',
    ]
    for (px, py), label in zip(pts, labels, strict=True):
        parts += [
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#0072B2"/>',
            f'<text x="{px:.1f}" y="{top+ih+22}" text-anchor="middle" '
            f'font-size="12" font-family="Arial">{label}</text>',
        ]
    parts.append(
        f'<text x="{left}" y="{height-15}" font-size="11" fill="#444">'
        "Archived rounded summary ONLY; not an original embedding/3D projection.</text></svg>"
    )
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    """Parse input/output paths for a recorded summary chart."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--x", required=True)
    parser.add_argument("--y", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    render_summary(args.source, args.output, x=args.x, y=args.y, title=args.title)


if __name__ == "__main__":
    main()
