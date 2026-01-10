# world_core/sandys_square.py

"""
SandySquare — coherence gating physics

Implements the minimal Trap → Transition → Escape logic
used by the Ledger and Manager.

This file MUST remain stable.
"""

from typing import Dict


def coherence_gate(
    sigma: float,
    z: float,
    persistence: float,
    threshold: float = 0.55,
) -> Dict[str, float]:
    """
    SandySquare gate.

    Inputs:
    - sigma: entropy / variability (0–1)
    - z: inhibition / structure (0–1)
    - persistence: stability over frames (0–1)

    Output:
    - coherence: final stability score
    - approved: boolean gate result
    """

    # Divergence = entropy restrained by structure
    divergence = sigma * (1.0 - z)

    # Coherence grows with persistence and restraint
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