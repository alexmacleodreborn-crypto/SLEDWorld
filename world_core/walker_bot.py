# world_core/walker_bot.py

import math
import random


class WalkerBot:
    """
    Physical world walker.

    - Moves continuously in XYZ space using world time
    - NEVER stops unless the world stops
    - Semantic location is derived from geometry only
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world  # READ-ONLY world reference

        # -----------------------------------------
        # Physical state
        # -----------------------------------------
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]

        self.speed = 1.2  # meters per minute

        # -----------------------------------------
        # Navigation state
        # -----------------------------------------
        self.target = None
        self.arrival_threshold = 0.5  # meters

        # -----------------------------------------
        # Observer-only semantics
        # -----------------------------------------
        self.current_area = None

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None

        # Choose initial destination
        self._pick_new_target()

        # Resolve initial area
        self._resolve_current_area()

    # =================================================
    # TARGET SELECTION (WORLD-DRIVEN)
    # =================================================

    def _pick_new_target(self):
        """
        Select a new random physical target from world places.
        No cognition. No preference.
        """
        places = list(self.world.places.values())
        if not places:
            self.target = None
            return

        place = random.choice(places)
        self.target = [
            float(place.position[0]),
            float(place.position[1]),
            float(place.position[2]),
        ]

    # =================================================
    # WORLD TICK
    # =================================================

    def tick(self, clock):
        now = clock.world_datetime

        if self._last_time is None:
            self._last_time = now
            return

        delta_seconds = (now - self._last_time).total_seconds()
        self._last_time = now

        if delta_seconds <= 0:
            return

        minutes = delta_seconds / 60.0

        self._move(minutes)
        self._resolve_current_area()

    def _move(self, minutes):
        if self.target is None:
            self._pick_new_target()
            return

        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        # -----------------------------------------
        # Arrival
        # -----------------------------------------
        if distance <= self.arrival_threshold:
            self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # SEMANTIC RESOLUTION (GEOMETRY ONLY)
    # =================================================

    def _resolve_current_area(self):
        xyz = tuple(self.position)

        # Rooms first (more specific)
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return

        # Places next
        for place in self.world.places.values():
            if place.contains_world_point(xyz):
                self.current_area = place.name
                return

        self.current_area = None

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "target_xyz": self.target,
            "current_area": self.current_area,
            "speed_m_per_min": self.speed,
        }