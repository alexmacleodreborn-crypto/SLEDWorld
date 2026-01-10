# world_core/ledger_event.py

from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class LedgerEvent:
    frame: int
    source: str
    entity: str
    kind: str                     # e.g. "percept", "interaction", "field", "structure", "symbol"
    payload: Dict[str, Any]
    confidence: float = 0.5
    signature: Optional[str] = None  # stable id hash later