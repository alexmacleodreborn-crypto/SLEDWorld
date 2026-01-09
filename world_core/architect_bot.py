# world_core/architect_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple
import math


@dataclass
class ArchitectBot:
    """
    Architect = structure inference only.
    Reads SYMBOLS and GEOMETRY summaries, proposes higher-order structures:
      BRICK -> WALL
      4 WALLs -> ROOM
    Does NOT read raw world objects directly (only summaries passed in).
    """

    name: str = "Architect-1"
    proposals: List[Dict[str, Any]] = field(default_factory=list)
    frame: int = 0

    def propose(self, frame: int, symbols: Dict[str, Any], geom: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.frame = frame
        self.proposals = []

        # Expect geom["planes"] like {"x": [...], "y": [...], "z": [...]}
        planes = geom.get("planes", {})
        x_planes = planes.get("x", [])
        y_planes = planes.get("y", [])

        # If we already have BRICK, we can propose WALLs along dominant planes
        have_brick = "BRICK" in symbols.get("types", {})
        if have_brick and (x_planes or y_planes):
            for p in x_planes:
                self.proposals.append({
                    "type": "WALL_PROPOSAL",
                    "axis": "x",
                    "coord": p["coord"],
                    "span": p.get("span", None),
                    "confidence": min(0.85 + 0.15 * p.get("support", 0.0), 0.99),
                    "frame": frame,
                })
            for p in y_planes:
                self.proposals.append({
                    "type": "WALL_PROPOSAL",
                    "axis": "y",
                    "coord": p["coord"],
                    "span": p.get("span", None),
                    "confidence": min(0.85 + 0.15 * p.get("support", 0.0), 0.99),
                    "frame": frame,
                })

        # If we have >=2 x-planes and >=2 y-planes, we can propose a ROOM enclosure
        # (This is the minimal enclosure logic: 4 bounding planes)
        if len(x_planes) >= 2 and len(y_planes) >= 2:
            # pick two strongest planes in each axis
            x_sorted = sorted(x_planes, key=lambda d: d.get("support", 0.0), reverse=True)[:2]
            y_sorted = sorted(y_planes, key=lambda d: d.get("support", 0.0), reverse=True)[:2]

            # Ensure separation exists (not same plane duplicated)
            if abs(x_sorted[0]["coord"] - x_sorted[1]["coord"]) > 0.5 and abs(y_sorted[0]["coord"] - y_sorted[1]["coord"]) > 0.5:
                width = abs(x_sorted[0]["coord"] - x_sorted[1]["coord"])
                depth = abs(y_sorted[0]["coord"] - y_sorted[1]["coord"])
                area = width * depth

                conf = 0.8
                # bump confidence if we already have WALL symbol confirmed
                if "WALL" in symbols.get("types", {}):
                    conf += 0.1
                # bump if area is reasonable (avoid degenerate boxes)
                if area > 4.0:
                    conf += 0.05

                self.proposals.append({
                    "type": "ROOM_PROPOSAL",
                    "bounds_2d": {
                        "x_min": min(x_sorted[0]["coord"], x_sorted[1]["coord"]),
                        "x_max": max(x_sorted[0]["coord"], x_sorted[1]["coord"]),
                        "y_min": min(y_sorted[0]["coord"], y_sorted[1]["coord"]),
                        "y_max": max(y_sorted[0]["coord"], y_sorted[1]["coord"]),
                    },
                    "confidence": min(conf, 0.99),
                    "frame": frame,
                })

        return list(self.proposals)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "architect",
            "name": self.name,
            "frame": self.frame,
            "num_proposals": len(self.proposals),
            "proposals_tail": self.proposals[-10:],
        }