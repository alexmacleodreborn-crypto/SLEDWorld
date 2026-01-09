# world_core/observer_bot.py

from __future__ import annotations
from typing import Dict, Any

class ObserverBot:
    """
    Global perception aggregator.
    - Sees object state
    - Sees light + hears sound (via room/object snapshots)
    - Records changes (diffs) between frames
    """
    def __init__(self, name: str):
        self.name = name
        self._last_seen: Dict[str, Any] = {}
        self._last_snapshot: Dict[str, Any] = {}
        self._frame = 0

    def observe(self, world):
        self._frame = world.frame

        seen = {}
        events = []

        # gather objects of interest: tv in any room
        for place in world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    for obj_name, obj in room.objects.items():
                        if hasattr(obj, "snapshot"):
                            o = obj.snapshot()
                        else:
                            o = {"name": getattr(obj, "name", obj_name)}
                        key = f"{room.name}:{obj_name}"
                        seen[key] = o

        # diff
        for key, now in seen.items():
            prev = self._last_seen.get(key)
            if prev is None:
                events.append({"type": "appear", "key": key})
            else:
                # compare some known fields if present
                for field in ("is_on", "light_color", "sound_level", "light_level"):
                    if field in now and field in prev and now[field] != prev[field]:
                        events.append({"type": "change", "key": key, "field": field, "from": prev[field], "to": now[field]})

        self._last_seen = seen

        self._last_snapshot = {
            "source": "observer",
            "name": self.name,
            "frame": self._frame,
            "events": events,
            "seen_objects": seen,
            "world_space": world.space.snapshot(),
        }

    def snapshot(self) -> Dict[str, Any]:
        return self._last_snapshot or {
            "source": "observer",
            "name": self.name,
            "frame": self._frame,
            "events": [],
            "seen_objects": {},
        }