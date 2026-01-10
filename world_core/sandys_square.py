# world_core/sandys_square.py

"""
SandySquare — coherence gating physics

Now supports:
- Scalar sigma
- Point-cloud sigma (list of recent events / points)
"""

from typing import Dict, Any, Optional, Union
import math


def _derive_sigma_from_points(points) -> float:
    """
    Derive entropy (sigma) from a set of points.

    Rule:
    - Empty or 1 point → low entropy
    - Widely spread points → high entropy
    """

    if not points or len(points) <= 1:
        return 0.05

    # If points are numeric, compute variance
    if all(isinstance(p, (int, float)) for p in points):
        mean = sum(points) / len(points)
        var = sum((p - mean) ** 2 for p in points) / len(points)
        return min(1.0, math.sqrt(var))

    # If points are dicts/events → entropy from diversity
    unique = len({str(p) for p in points})
    return min(1.0, unique / max(1, len(points)))


def coherence_gate(
    sigma: Optional[Union[float, list]] = None,
    z: Optional[float] = None,
    persistence: Optional[float] = None,
    threshold: float = 0.55,
    metrics: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    SandySquare coherence gate.

    Accepts:
    - coherence_gate(sigma, z, persistence)
    - coherence_gate(point_list, size=...)
    - coherence_gate(metrics=dict)
    """

    # ---------------------------------------------
    # 1. Handle positional point-cloud sigma
    # ---------------------------------------------
    if isinstance(sigma, (list, tuple)):
        sigma = _derive_sigma_from_points(sigma)

    # ---------------------------------------------
    # 2. Pull from metrics dict if provided
    # ---------------------------------------------
    if isinstance(metrics, dict):
        sigma = metrics.get("sigma", sigma)
        z = metrics.get("z", z)
        persistence = metrics.get("persistence", persistence)

    # ---------------------------------------------
    # 3. Pull from kwargs
    # ---------------------------------------------
    sigma = kwargs.get("sigma", sigma)
    z = kwargs.get("z", z)
    persistence = kwargs.get("persistence", persistence)

    # ---------------------------------------------
    # 4. Fail-closed defaults
    # ---------------------------------------------
    if sigma is None:
        sigma = 1.0
    if z is None:
        z = 0.0
    if persistence is None:
        persistence = 0.0

    # Clamp
    sigma = float(max(0.0, min(1.0, sigma)))
    z = float(max(0.0, min(1.0, z)))
    persistence = float(max(0.0, min(1.0, persistence)))

    # ---------------------------------------------
    # 5. SandySquare physics
    # ---------------------------------------------
    divergence = sigma * (1.0 - z)
    coherence = max(
        0.0,
        min(
            1.0,
            (1.0 - divergence) * (0.5 + 0.5 * persistence),
        ),
    )

    approved = coherence >= threshold

    return {
        "sigma": round(sigma, 4),
        "z": round(z, 4),
        "persistence": round(persistence, 4),
        "divergence": round(divergence, 4),
        "coherence": round(coherence, 4),
        "approved": approved,
    }