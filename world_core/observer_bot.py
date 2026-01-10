# world_core/observer_bot.py

from typing import Dict, Any

class ObserverBot:
    """
    Passive perception. No interaction.
    Reports global + nearest-room sensory summary.
    """
    def __init__(self, name="Observer-1"):
        self.name = name
        self.last = {}

    def observe(self, world):
        # v1: find the living room and read its sound/light
        room_snap = None
        tv_state = None

        for place in world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    rs = room.snapshot()
                    if rs.get("room_type") == "living_room":
                        room_snap = rs
                        tv = rs.get("objects", {}).get("tv")
                        if isinstance(tv, dict):
                            tv_state = tv.get("is_on")
                        break

        self.last = {
            "source": "observer",
            "entity": self.name,
            "name": self.name,
            "frame": world.frame,
            "world_space": world.space.snapshot(),
            "seen_light_level": (room_snap.get("light_level") if room_snap else 0.0),
            "seen_light_color": (room_snap.get("light_color") if room_snap else "none"),
            "heard_sound_level": (room_snap.get("sound_level") if room_snap else 0.0),
            "tv_state": tv_state,
            "current_area": (room_snap.get("name") if room_snap else "world"),
            "position_xyz": None,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.last or {"source":"observer","entity":self.name,"name":self.name,"frame":0}