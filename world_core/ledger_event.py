# world_core/ledger_event.py

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class LedgerEvent:
    """
    Canonical world event.

    This is the ONLY structure allowed to cross
    from perception into cognition.

    Immutable once created.
    """

    # ---------------------------------
    # Identity
    # ---------------------------------
    event_id: int
    frame: int
    source: str              # observer | walker | scout | surveyor
    entity: Optional[str]    # tv | wall | room | sound | light | unknown

    # ---------------------------------
    # Spatial grounding (NO TIME ASSUMPTION)
    # ---------------------------------
    position_xyz: Optional[tuple] = None
    bounds: Optional[Dict[str, Any]] = None

    # ---------------------------------
    # Sensory channels
    # ---------------------------------
    sound_level: Optional[float] = None
    light_level: Optional[float] = None
    light_color: Optional[str] = None

    # ---------------------------------
    # Shape & structure
    # ---------------------------------
    shape_signature: Optional[Dict[str, Any]] = None
    surface_signature: Optional[Dict[str, Any]] = None

    # ---------------------------------
    # Change detection
    # ---------------------------------
    delta: Dict[str, Any] = field(default_factory=dict)

    # ---------------------------------
    # Stability & gating
    # ---------------------------------
    persistence_count: int = 1
    confidence: float = 0.0

    # ---------------------------------
    # Semantic unlocks (EMPTY INITIALLY)
    # ---------------------------------
    symbol: Optional[str] = None
    approved: bool = False