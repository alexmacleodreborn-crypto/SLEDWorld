# world_core/sandys_square.py

"""
SandySquare — coherence gating physics

Freeze-safe gate function.
Accepts:
- coherence_gate(sigma=..., z=..., persistence=...)
- coherence_gate({"sigma":..., "z":..., "persistence":...})
- coherence_gate(metrics=<dict>)
- coherence_gate(**kwargs) with extra fields (size, area, volume, etc)

If required values are missing, it FAILS CLOSED (approved=False) instead of crashing.
"""

from typing import Dict, Any, Optional, Union


def coherence_gate(
    sigma: Optional[float] = None,
    z: Optional[float] = None,
    persistence: Optional[float] = None,
    threshold: float = 0.55,
    metrics: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    SandySquare gate.

    Required conceptual inputs (0–1):
    - sigma: entropy / variability
    - z: inhibition / structure
    - persistence: stability over frames

    Supports being called with a single positional dict (args[0]) or metrics=...
    Extra kwargs are accepted and ignored unless later used.
    """

    # -------------------------------------------------
    # 1) If called with a single positional dict, treat it as metrics
    # -------------------------------------------------
    if metrics is None and len(args) == 1 and isinstance(args[0], dict):
        metrics = args[0]

    # -------------------------------------------------
    # 2) Pull values from metrics dict if provided
    # -------------------------------------------------
    if isinstance(metrics, dict):
        if sigma is None:
            sigma = metrics.get("sigma", metrics.get("Sigma", metrics.get("entropy")))
        if z is None:
            z = metrics.get("z", metrics.get("Z", metrics.get("trap")))
        if persistence is None:
            persistence = metrics.get("persistence", metrics.get("stable", metrics.get("stability")))

    # -------------------------------------------------
    # 3) Pull values from kwargs (common in pipelines)
    # -------------------------------------------------
    if sigma is None:
        sigma = kwargs.get("sigma", kwargs.get("Sigma"))
    if z is None:
        z = kwargs.get("z", kwargs.get("Z"))
    if persistence is None:
        persistence = kwargs.get("persistence", kwargs.get("stability"))

    # -------------------------------------------------
    # 4) Fail-closed if still missing
    # -------------------------------------------------
    missing = []
    if sigma is None:
        missing.append("sigma")
        sigma = 1.0  # worst-case entropy
    if z is None:
        missing.append("z")
        z = 0.0      # no structure
    if persistence is None:
        missing.append("persistence")
        persistence = 0.0  # no stability

    # Clamp to [0,1] safely
    sigma = float(max(0.0, min(1.0, sigma)))
    z = float(max(0.0, min(1.0, z)))
    persistence = float(max(0.0, min(1.0, persistence)))

    # -------------------------------------------------
    # 5) Core SandySquare physics
    # -------------------------------------------------
    divergence = sigma * (1.0 - z)
    coherence = max(
        0.0,
        min(
            1.0,
            (1.0 - divergence) * (0.5 + 0.5 * persistence),
        ),
    )

    approved = (coherence >= float(threshold)) and (len(missing) == 0)

    out = {
        "sigma": round(sigma, 4),
        "z": round(z, 4),
        "persistence": round(persistence, 4),
        "divergence": round(divergence, 4),
        "coherence": round(coherence, 4),
        "approved": approved,
    }

    if missing:
        out["missing_inputs"] = missing
        out["note"] = "Gate failed closed due to missing inputs."

    return out