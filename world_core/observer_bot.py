# world_core/observer_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ObserverBot:
    """
    Passive perception.
    - No physics
    - No movement
    - Just reads world state and emits a perception snapshot
    """
    name: str = "Observer-1"
    frames_observed: int = 0
    seen_places: Dict[str, int] = field(default_factory=dict)
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def observe(self, world):
        self.frames_observed += 1

        # mark places “seen”
        for p in world.places.values():
            self.seen_places[p.name] = self.seen_places.get(p.name, 0) + 1

        # capture environment fields (if present)
        space = getattr(world, "space", None)
        space_snap = space.snapshot() if space and hasattr(space, "snapshot") else None

        # capture object summary (TV state etc)
        objects = []
        for place in world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if hasattr(room, "objects"):
                        for obj_name, obj in room.objects.items():
                            # try to show TV is_on if present
                            obj_state = {"place": place.name, "room": room.name, "name": obj_name}
                            if hasattr(obj, "is_on"):
                                obj_state["is_on"] = bool(getattr(obj, "is_on"))
                            if hasattr(obj, "position"):
                                obj_state["position"] = getattr(obj, "position")
                            objects.append(obj_state)

        frame = getattr(space, "frame_counter", self.frames_observed)

        self.last_snapshot = {
            "source": "observer",
            "name": self.name,
            "frame": int(frame),
            "frames_observed": int(self.frames_observed),
            "seen_places": dict(self.seen_places),
            "world_fields": space_snap,
            "objects_seen": objects[:50],  # cap
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "observer",
            "name": self.name,
            "frame": self.frames_observed,
            "frames_observed": self.frames_observed,
            "seen_places": self.seen_places,
        }