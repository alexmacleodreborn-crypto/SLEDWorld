# world_core/sandys_square.py

"""
SandySquare — coherence gating physics

Implements the minimal Trap → Transition → Escape logic.
Forward-compatible with evolving metrics.
"""

from typing import Dict, Any


def coherence_gate(
    sigma: float,
    z: float,
    persistence: float,
    threshold: float = 0.55,
    **kwargs: Any,          # ← absorbs size, area, volume, etc
) -> Dict[str, float]:
    """
    SandySquare gate.

    Required inputs:
    - sigma: entropy / variability (0–1)
    - z: inhibition / structure (0–1)
    - persistence: stability over frames (0–1)

    Optional (ignored unless later used):
    - size
    - area
    - volume
    - count
    - anything else future bots attach
    """

    # Divergence = entropy restrained by structure
    divergence = sigma * (1.0 - z)

    # Coherence grows with persistence
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