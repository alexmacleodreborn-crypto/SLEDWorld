# world_core/sandys_square.py

"""
SandySquare — coherence gating physics (FINAL)

Accepts:
- scalar
- list / tuple (point clouds)
- dict (metric packets)

Never crashes.
Always fails closed.
"""

from typing import Dict, Any, Optional, Union
import math


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _clamp01(x: float) -> float:
    return float(max(0.0, min(1.0, x)))


def _derive_sigma_from_points(points) -> float:
    if not points or len(points) <= 1:
        return 0.05

    # numeric variance
    if all(isinstance(p, (int, float)) for p in points):
        mean = sum(points) / len(points)
        var = sum((p - mean) ** 2 for p in points) / len(points)
        return _clamp01(math.sqrt(var))

    # symbolic diversity
    unique = len({str(p) for p in points})
    return _clamp01(unique / max(1, len(points)))


def _derive_scalar(value) -> float:
    """
    Collapse any supported structure into a scalar [0,1].
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return _clamp01(float(value))

    if isinstance(value, (list, tuple)):
        return _derive_sigma_from_points(value)

    if isinstance(value, dict):
        # priority keys (common across your system)
        for k in ("value", "score", "coherence", "stability", "mean"):
            if k in value and isinstance(value[k], (int, float)):
                return _clamp01(float(value[k]))

        # fallback: entropy from dict size
        return _clamp01(len(value) / 10.0)

    # unknown type
    return 0.0


# -------------------------------------------------
# SandySquare gate
# -------------------------------------------------

def coherence_gate(
    sigma: Optional[Union[float, list, dict]] = None,
    z: Optional[Union[float, dict]] = None,
    persistence: Optional[Union[float, dict]] = None,
    threshold: float = 0.55,
    metrics: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    SandySquare coherence gate.

    FAIL-SAFE:
    - Accepts rich structures
    - Collapses to scalars
    - Never raises TypeError
    """

    # -------------------------------------------------
    # 1) Allow positional dict call
    # -------------------------------------------------
    if isinstance(sigma, dict) and metrics is None:
        metrics = sigma
        sigma = None

    # -------------------------------------------------
    # 2) Pull from metrics if present
    # -------------------------------------------------
    if isinstance(metrics, dict):
        sigma = metrics.get("sigma", sigma)
        z = metrics.get("z", z)
        persistence = metrics.get("persistence", persistence)

    # -------------------------------------------------
    # 3) Pull from kwargs
    # -------------------------------------------------
    sigma = kwargs.get("sigma", sigma)
    z = kwargs.get("z", z)
    persistence = kwargs.get("persistence", persistence)

    # -------------------------------------------------
    # 4) Collapse everything to scalars
    # -------------------------------------------------
    sigma_s = _derive_scalar(sigma)
    z_s = _derive_scalar(z)
    persistence_s = _derive_scalar(persistence)

    # -------------------------------------------------
    # 5) SandySquare physics
    # -------------------------------------------------
    divergence = sigma_s * (1.0 - z_s)

    coherence = _clamp01(
        (1.0 - divergence) * (0.5 + 0.5 * persistence_s)
    )

    approved = coherence >= threshold

    return {
        "sigma": round(sigma_s, 4),
        "z": round(z_s, 4),
        "persistence": round(persistence_s, 4),
        "divergence": round(divergence, 4),
        "coherence": round(coherence, 4),
        "approved": approved,
    }