# world_core/scout_bot.py

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class ScoutBot:
    """
    Salience scout.

    Monitors ONE feature stream (sound / light / shape).
    Reports persistence and change.
    """

    name: str
    focus: str = "shape"          # sound | light | shape
    target: Optional[str] = None
    max_frames: int = 200

    active: bool = True
    frames: int = 0

    last_value: Optional[Any] = None
    persistence: int = 0

    last_snapshot: Dict[str, Any] = field(default_factory=dict)

    # =================================================
    # COMPATIBILITY LAYER (IMPORTANT)
    # =================================================
    def __init__(self, name: str, **kwargs):
        self.name = name

        # Accept ANY future parameters safely
        self.focus = kwargs.get("focus", "shape")
        self.target = kwargs.get("target", None)
        self.max_frames = int(kwargs.get("max_frames", 200))

        self.active = True
        self.frames = 0
        self.last_value = None
        self.persistence = 0
        self.last_snapshot = {}

    # =================================================
    # Observation
    # =================================================

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        value = self._extract_value(world)
        if value is None:
            return

        if value == self.last_value:
            self.persistence += 1
            delta = 0
        else:
            self.persistence = 1
            delta = 1

        self.last_value = value

        self.last_snapshot = {
            "source": "scout",
            "name": self.name,
            "focus": self.focus,
            "target": self.target,
            "frame": self.frames,
            "value": value,
            "delta": delta,
            "persistence": self.persistence,
            "active": self.active,
        }

    # =================================================
    # Feature extraction
    # =================================================

    def _extract_value(self, world):
        if self.focus == "sound":
            total = 0.0
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if hasattr(room, "get_sound_level"):
                            total += room.get_sound_level()
            return round(total, 3)

        if self.focus == "light":
            total = 0.0
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        for obj in room.objects.values():
                            if hasattr(obj, "light"):
                                total += obj.light.level()
            return round(total, 3)

        if self.focus == "shape":
            count = 0
            for place in world.places.values():
                if hasattr(place, "bounds"):
                    count += 1
                if hasattr(place, "rooms"):
                    count += len(place.rooms)
            return count

        return None

    # =================================================
    # Snapshot
    # =================================================

    def snapshot(self) -> Dict[str, Any]:
        return self.last_snapshot or {
            "source": "scout",
            "name": self.name,
            "focus": self.focus,
            "active": self.active,
            "frame": self.frames,
        }