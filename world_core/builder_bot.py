# world_core/builder_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List
import math


@dataclass
class BuilderBot:
    """
    Builder = validation only.
    Takes Architect proposals + Surveyor geometry summary and produces validation scores.
    Does NOT modify the world.

    Output is used by the Ledger to promote symbols.
    """

    name: str = "Builder-1"
    validations: List[Dict[str, Any]] = field(default_factory=list)
    frame: int = 0

    def validate(self, frame: int, proposals: List[Dict[str, Any]], geom: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.frame = frame
        self.validations = []

        planes = geom.get("planes", {})
        x_planes = {p["coord"]: p for p in planes.get("x", [])}
        y_planes = {p["coord"]: p for p in planes.get("y", [])}

        for prop in proposals:
            if prop["type"] == "WALL_PROPOSAL":
                axis = prop["axis"]
                coord = prop["coord"]
                # Find nearest detected plane on that axis
                plane_map = x_planes if axis == "x" else y_planes
                if not plane_map:
                    score = 0.0
                else:
                    nearest = min(plane_map.keys(), key=lambda c: abs(c - coord))
                    support = plane_map[nearest].get("support", 0.0)
                    dist = abs(nearest - coord)
                    score = max(0.0, min(1.0, support * math.exp(-dist)))

                self.validations.append({
                    "type": "WALL_VALIDATION",
                    "axis": axis,
                    "coord": coord,
                    "score": round(score, 3),
                    "frame": frame,
                })

            elif prop["type"] == "ROOM_PROPOSAL":
                b = prop["bounds_2d"]
                # Validate by checking existence of planes near each boundary
                x_min = b["x_min"]; x_max = b["x_max"]
                y_min = b["y_min"]; y_max = b["y_max"]

                def best_plane_score(plane_coords, target):
                    if not plane_coords:
                        return 0.0
                    nearest = min(plane_coords, key=lambda c: abs(c - target))
                    # distance penalty
                    dist = abs(nearest - target)
                    support = (x_planes.get(nearest) or y_planes.get(nearest) or {}).get("support", 0.0)
                    return max(0.0, min(1.0, support * math.exp(-dist)))

                sx1 = best_plane_score(list(x_planes.keys()), x_min)
                sx2 = best_plane_score(list(x_planes.keys()), x_max)
                sy1 = best_plane_score(list(y_planes.keys()), y_min)
                sy2 = best_plane_score(list(y_planes.keys()), y_max)

                score = (sx1 + sx2 + sy1 + sy2) / 4.0
                self.validations.append({
                    "type": "ROOM_VALIDATION",
                    "bounds_2d": b,
                    "score": round(score, 3),
                    "frame": frame,
                })

        return list(self.validations)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "builder",
            "name": self.name,
            "frame": self.frame,
            "num_validations": len(self.validations),
            "validations_tail": self.validations[-10:],
        }