# world_core/profiles/remote_profile.py

from __future__ import annotations

class RemoteProfile:
    def __init__(self, name, position, tv):
        self.name = name
        self.position = position
        self.tv = tv

    def power_toggle(self):
        return self.tv.power_toggle()

    def snapshot(self):
        return {
            "name": self.name,
            "type": "remote",
            "position": self.position,
            "bound_to": getattr(self.tv, "name", "tv"),
        }