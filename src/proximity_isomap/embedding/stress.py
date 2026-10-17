"""Stress evaluator separating within- and between-component distortions."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import pdist

from proximity_isomap.distances.hybrid import HybridDissimilarities


@dataclass(frozen=True)
class StressBreakdown:
    """Normalized stress components (None if group is empty or degenerate)."""

    within: float | None
    between: float | None
    combined: float
    within_pairs: int
    between_pairs: int


def normalized_hybrid_stress(
    embedding: NDArray[np.floating],
    dissimilarities: HybridDissimilarities,
    alpha: float = 0.5,
) -> StressBreakdown:
    """Evaluate the normalized hybrid stress of a *given* embedding.

    This function does not optimize coordinates. ``alpha`` is the weight for
    within-component graph-geodesic stress; ``1-alpha`` for between-component
    ambient-distance stress. Undefined/degenerate groups are omitted, and
    active weights are renormalized. If no positive-weight group is defined,
    raise ``ValueError``.

    Parameters
    ----------
    embedding:
        Finite coordinates with shape ``(n_samples, n_components)``.
    dissimilarities:
        Square target dissimilarity and same-component pair mask.
    alpha:
        Relative weight on normalized intracomponent graph stress in [0, 1].

    Returns
    -------
    StressBreakdown
        The two component stresses (possibly ``None``), their normalized
        weighted combination, and pair counts.

    Raises
    ------
    ValueError
        For incompatible dimensions, invalid values, or no active pair group.

    Notes
    -----
    Denominators are sums of squared target distances. Only strictly
    positive-denominator groups contribute to the combined objective.
    """
    y = np.asarray(embedding, dtype=float)
    target = np.asarray(dissimilarities.target, dtype=float)
    same = np.asarray(dissimilarities.same_component, dtype=bool)
    if y.ndim != 2 or y.shape[1] < 1 or not np.isfinite(y).all():
        raise ValueError("embedding must be a finite (n, d) array")
    if target.shape != (len(y), len(y)) or same.shape != target.shape:
        raise ValueError("dissimilarity and embedding shapes do not match")
    if not np.isfinite(target).all() or (target < 0).any():
        raise ValueError("target dissimilarities must be finite and nonnegative")
    if not np.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("alpha must be between zero and one")

    i, j = np.triu_indices(len(y), k=1)
    actual = pdist(y)
    desired = target[i, j]
    within_mask = same[i, j]

    def group_stress(mask: NDArray[np.bool_]) -> float | None:
        if not np.any(mask):
            return None
        denom = float(np.square(desired[mask]).sum())
        if denom <= 0:
            return None
        return float(np.square(actual[mask] - desired[mask]).sum() / denom)

    inside = group_stress(within_mask)
    outside = group_stress(~within_mask)
    active = [(alpha, inside), (1.0 - alpha, outside)]
    weight_sum = sum(weight for weight, value in active if value is not None)
    if weight_sum <= 0:
        raise ValueError("no nondegenerate pair group has positive weight")
    combined = sum(weight * value for weight, value in active if value is not None)
    return StressBreakdown(
        within=inside,
        between=outside,
        combined=float(combined / weight_sum),
        within_pairs=int(within_mask.sum()),
        between_pairs=int((~within_mask).sum()),
    )
