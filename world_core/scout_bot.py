# world_core/scout_bot.py

class ScoutBot:
    """
    Modality-specific scout.

    Modes:
    - "sound" : listens for sound field changes
    - "light" : listens for light field changes
    - "shape" : listens for object presence (optional later)

    Scouts do NOT think.
    Scouts only report deltas to the ledger.
    """

    def __init__(
        self,
        name: str,
        mode: str = "sound",
        max_frames: int = 200,
    ):
        self.name = name
        self.mode = mode
        self.max_frames = max_frames

        self.frames = 0
        self.active = True

        self.last_snapshot = {}
        self.last_value = None

    # -------------------------------------------------
    # Observe world
    # -------------------------------------------------

    def observe(self, world):
        if not self.active:
            return

        self.frames += 1
        if self.frames > self.max_frames:
            self.active = False
            return

        value = None

        # -------------------------
        # SOUND MODE
        # -------------------------
        if self.mode == "sound":
            total = 0.0
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if hasattr(room, "get_sound_level"):
                            total += room.get_sound_level()
            value = round(total, 3)

        # -------------------------
        # LIGHT MODE
        # -------------------------
        elif self.mode == "light":
            total = 0.0
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        for obj in getattr(room, "objects", {}).values():
                            if hasattr(obj, "light"):
                                total += obj.light.level()
            value = round(total, 3)

        # -------------------------
        # SHAPE MODE (reserved)
        # -------------------------
        elif self.mode == "shape":
            value = len(world.places)

        # -------------------------
        # Only report changes
        # -------------------------
        if value != self.last_value:
            self.last_value = value
            self.last_snapshot = {
                "source": "scout",
                "name": self.name,
                "mode": self.mode,
                "value": value,
                "frame": world.frame,
                "active": self.active,
            }

    # -------------------------------------------------
    # Snapshot
    # -------------------------------------------------

    def snapshot(self):
        return self.last_snapshot if self.last_snapshot else None