# world_core/observer_bot.py

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class ObserverBot:
    """
    Passive perception.
    Reports fields (sound/light) and stable object snapshots.
    No semantics required.
    """

    name: str = "Observer-1"
    frames_observed: int = 0
    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    def observe(self, world):
        self.frames_observed += 1
        frame = int(getattr(getattr(world, "space", None), "frame_counter", self.frames_observed))

        # Global fields
        space = getattr(world, "space", None)
        space_snap = space.snapshot() if space and hasattr(space, "snapshot") else None

        # Field events discovered in rooms/objects
        fields: List[dict] = []
        objects: List[dict] = []

        for place in world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                # Room-level fields
                if hasattr(room, "get_sound_level"):
                    try:
                        fields.append({
                            "type": "sound",
                            "scope": "room",
                            "room": room.name,
                            "level": float(room.get_sound_level()),
                        })
                    except Exception:
                        pass

                if hasattr(room, "get_light_level"):
                    try:
                        lo = room.get_light_level()
                        fields.append({
                            "type": "light",
                            "scope": "room",
                            "room": room.name,
                            "intensity": float(lo.get("intensity", 0.0)),
                            "color": lo.get("color", "none"),
                        })
                    except Exception:
                        pass

                # Object snapshots
                objs = getattr(room, "objects", {})
                for obj_name, obj in objs.items():
                    if hasattr(obj, "snapshot"):
                        snap = obj.snapshot()
                    else:
                        snap = {"name": obj_name, "repr": str(obj)}

                    # Add light/sound fields if present
                    if hasattr(obj, "get_light_output"):
                        try:
                            ls = obj.get_light_output()
                            fields.append({
                                "type": "light",
                                "scope": "object",
                                "room": room.name,
                                "object": obj_name,
                                "intensity": float(ls.get("intensity", 0.0)),
                                "color": ls.get("color", "none"),
                            })
                        except Exception:
                            pass

                    if hasattr(obj, "get_sound_level"):
                        try:
                            fields.append({
                                "type": "sound",
                                "scope": "object",
                                "room": room.name,
                                "object": obj_name,
                                "level": float(obj.get_sound_level()),
                            })
                        except Exception:
                            pass

                    objects.append({
                        "room": room.name,
                        "object": obj_name,
                        "snapshot": snap,
                    })

        self.last_snapshot = {
            "source": "observer",
            "name": self.name,
            "frame": frame,
            "world_space": space_snap,
            "fields": fields[:200],
            "objects": objects[:200],
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "observer",
            "name": self.name,
            "frame": self.frames_observed,
            "fields": [],
            "objects": [],
        }