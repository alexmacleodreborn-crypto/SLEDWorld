# world_core/observer_bot.py

import math


class ObserverBot:
    """
    Passive perception bot.
    No physics. No interaction.
    It "observes" the world each frame and reports signals.

    Strategy:
      - Anchor perception around Walker position (if present)
      - Resolve room/place from that position
      - Read room signals (light + sound) and report them
    """

    def __init__(self, name: str = "Observer-1"):
        self.name = name
        self.frames_observed = 0

        self.current_area = "world"
        self.current_bounds = None

        self.heard_sound_level = 0.0
        self.seen_light = {"intensity": 0.0, "color": "none"}

        self.seen_places = {}
        self.ledger = []

    def _distance(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

    def observe(self, world):
        self.frames_observed += 1

        walker_pos = None
        for a in getattr(world, "agents", []):
            if a.__class__.__name__ == "WalkerBot":
                walker_pos = tuple(getattr(a, "position", (0.0, 0.0, 0.0)))
                break

        # Fallback: observer just "sees" all places
        places = getattr(world, "places", {}) or {}
        for pname in places.keys():
            self.seen_places[pname] = self.seen_places.get(pname, 0) + 1

        self.current_area = "world"
        self.current_bounds = None
        self.heard_sound_level = 0.0
        self.seen_light = {"intensity": 0.0, "color": "none"}

        # If we have walker position, resolve current room/place and read signals
        if walker_pos is not None:
            # Try rooms first
            for place in places.values():
                rooms = getattr(place, "rooms", None)
                if not rooms:
                    continue
                for room in rooms.values():
                    if hasattr(room, "contains_world_point") and room.contains_world_point(walker_pos):
                        self.current_area = getattr(room, "name", "room")
                        self.current_bounds = getattr(room, "bounds", None)

                        rs = room.snapshot()
                        sig = rs.get("signals", {})
                        self.heard_sound_level = float(sig.get("sound", 0.0) or 0.0)
                        self.seen_light = sig.get("light") or {"intensity": 0.0, "color": "none"}

                        self.ledger.append({
                            "frame": self.frames_observed,
                            "event": "observe_room",
                            "area": self.current_area,
                            "sound": round(self.heard_sound_level, 3),
                            "light": self.seen_light,
                        })
                        return

            # Else resolve place
            for place in places.values():
                if hasattr(place, "contains_world_point") and place.contains_world_point(walker_pos):
                    self.current_area = getattr(place, "name", "place")
                    self.current_bounds = getattr(place, "bounds", None)

                    # Place signal fallback: compute from rooms if any
                    sound = 0.0
                    best_light = {"intensity": 0.0, "color": "none"}
                    rooms = getattr(place, "rooms", None)
                    if rooms:
                        for room in rooms.values():
                            rs = room.snapshot()
                            sig = rs.get("signals", {})
                            sound += float(sig.get("sound", 0.0) or 0.0)
                            lt = sig.get("light") or {"intensity": 0.0, "color": "none"}
                            if float(lt.get("intensity", 0.0) or 0.0) > float(best_light.get("intensity", 0.0) or 0.0):
                                best_light = lt

                    self.heard_sound_level = min(sound, 1.0)
                    self.seen_light = best_light

                    self.ledger.append({
                        "frame": self.frames_observed,
                        "event": "observe_place",
                        "area": self.current_area,
                        "sound": round(self.heard_sound_level, 3),
                        "light": self.seen_light,
                    })
                    return

        # Global fallback
        self.ledger.append({
            "frame": self.frames_observed,
            "event": "observe_world",
            "area": self.current_area,
            "sound": 0.0,
            "light": {"intensity": 0.0, "color": "none"},
        })

    def snapshot(self):
        return {
            "source": "observer",
            "type": "observer",
            "name": self.name,
            "frame": self.frames_observed,
            "current_area": self.current_area,
            "bounds": self.current_bounds,
            "signals": {
                "sound": round(self.heard_sound_level, 3),
                "light": self.seen_light,
            },
            "seen_places": dict(self.seen_places),
            "ledger_tail": self.ledger[-10:],
        }