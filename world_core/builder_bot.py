# world_core/builder_bot.py

from __future__ import annotations
from typing import Dict, Any, List
import numpy as np

class BuilderBot:
    """
    Validates architect proposals against surveyor geometry.
    Confirms only when evidence supports it.
    """
    def validate(self, proposals: List[Dict[str, Any]], ledger, surveyor) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []

        surv = surveyor.snapshot()
        aerial = surv.get("aerial_grid") if isinstance(surv, dict) else None

        for p in proposals:
            prop = p.get("proposal")

            if prop in ("WALL", "ROOM"):
                if aerial is None:
                    out.append({"source": "builder", "structure": prop, "status": "rejected", "match": 0.0, "reason": "no_aerial"})
                    continue

                arr = np.array(aerial, dtype=int)
                solid = int(arr.sum())

                # crude heuristic: if there is a non-trivial amount of solid, confirm WALL
                if prop == "WALL":
                    match = min(1.0, solid / 200.0)
                    status = "confirmed" if match >= 0.25 else "rejected"
                    out.append({"source": "builder", "structure": "WALL", "status": status, "match": round(match, 3)})
                    continue

                # for ROOM: we need hollow enclosed areas (some solids, some empties)
                if prop == "ROOM":
                    empties = int((arr == 0).sum())
                    total = arr.size
                    hollow_ratio = empties / float(total) if total else 0.0
                    # confirm if there is both structure and hollow (avoid all-solid or all-empty)
                    match = min(1.0, (solid / 200.0) * (hollow_ratio))
                    status = "confirmed" if (solid > 150 and hollow_ratio > 0.5) else "rejected"
                    out.append({"source": "builder", "structure": "ROOM", "status": status, "match": round(match, 3)})
                    continue

            if prop == "STATEFUL_OBJECT":
                # confirm if TV confidence exists in ledger
                symbols = getattr(ledger, "symbols", {}) or {}
                tvc = symbols.get("TV", {}).get("confidence", 0.0)
                status = "confirmed" if tvc >= 0.55 else "rejected"
                out.append({"source": "builder", "structure": "STATEFUL_OBJECT", "status": status, "match": round(float(tvc), 3)})
                continue

        return out