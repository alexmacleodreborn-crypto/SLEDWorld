# world_core/walker_bot.py

import math


class WalkerBot:
    """
    Physical world walker.

    - Moves continuously in XYZ space using world time
    - Has NO symbolic knowledge
    - Semantic location (room / park / area) is DERIVED
      purely from world geometry
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world  # READ-ONLY reference to world state

        # -----------------------------------------
        # Physical state
        # -----------------------------------------
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]  # XYZ meters

        self.speed = 1.2  # meters per minute (walking speed)

        # -----------------------------------------
        # Navigation state
        # -----------------------------------------
        self.target = None
        self.arrival_threshold = 0.5  # meters

        # -----------------------------------------
        # Observer-only semantics (derived, never driving)
        # -----------------------------------------
        self.current_area = None

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None

        # Resolve initial area
        self._resolve_current_area()

    # =================================================
    # NAVIGATION
    # =================================================

    def set_target(self, xyz):
        """
        Assign a physical destination in world space.
        """
        self.target = [
            float(xyz[0]),
            float(xyz[1]),
            float(xyz[2]),
        ]

    # =================================================
    # WORLD TICK
    # =================================================

    def tick(self, clock):
        """
        Advance the walker using world time.
        """
        now = clock.world_datetime

        # Initialise time anchor
        if self._last_time is None:
            self._last_time = now
            return

        delta_seconds = (now - self._last_time).total_seconds()
        self._last_time = now

        if delta_seconds <= 0:
            return

        minutes = delta_seconds / 60.0

        # Move physically if a target exists
        if self.target is not None:
            self._move(minutes)

        # ALWAYS resolve semantic area after movement
        self._resolve_current_area()

    def _move(self, minutes):
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        # -----------------------------------------
        # Arrival check
        # -----------------------------------------
        if distance <= self.arrival_threshold:
            self.target = None
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
        """
        Determine which room or place the walker is inside,
        based purely on world geometry.
        """

        xyz = tuple(self.position)

        # -----------------------------------------
        # Check rooms first (most specific)
        # -----------------------------------------
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return

        # -----------------------------------------
        # Fallback to place volumes
        # -----------------------------------------
        for place in self.world.places.values():
            if place.contains_world_point(xyz):
                self.current_area = place.name
                return

        # -----------------------------------------
        # Outside all known areas
        # -----------------------------------------
        self.current_area = None

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": [
                round(self.position[0], 2),
                round(self.position[1], 2),
                round(self.position[2], 2),
            ],
            "target_xyz": self.target,
            "current_area": self.current_area,
            "speed_m_per_min": self.speed,
        }