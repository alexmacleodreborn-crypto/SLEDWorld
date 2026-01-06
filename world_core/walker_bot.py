# world_core/walker_bot.py

import math
import random


class WalkerBot:
    """
    Physical world walker.

    Rules:
    - Moves continuously in XYZ using world time
    - NEVER stops
    - Semantic location is ALWAYS defined
    - Semantics are DERIVED from geometry only
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world  # READ-ONLY reference

        # -----------------------------------------
        # Physical state
        # -----------------------------------------
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]

        self.speed = 1.2  # meters per minute
        self.arrival_threshold = 0.5

        # -----------------------------------------
        # Navigation
        # -----------------------------------------
        self.target = None

        # -----------------------------------------
        # Semantic state (ALWAYS SET)
        # -----------------------------------------
        self.current_area = "world"

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None

        # Initial destination
        self._pick_new_target()
        self._resolve_current_area()

    # =================================================
    # TARGET SELECTION (VOLUME-AWARE)
    # =================================================

    def _pick_new_target(self):
        """
        Select a random physical point inside:
        - a room (preferred)
        - otherwise inside a place
        """
        rooms = []
        places = []

        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                rooms.extend(place.rooms.values())
            places.append(place)

        # Prefer rooms if available
        if rooms:
            room = random.choice(rooms)
            self.target = self._random_point_in_bounds(room.bounds)
            return

        # Fallback: place volume
        if places:
            place = random.choice(places)
            self.target = self._random_point_in_bounds(place.bounds)
            return

        self.target = None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
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

        if distance <= self.arrival_threshold:
            self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # SEMANTIC RESOLUTION (NEVER NULL)
    # =================================================

    def _resolve_current_area(self):
        xyz = tuple(self.position)

        # 1️⃣ Rooms (most specific)
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return

        # 2️⃣ Places
        for place in self.world.places.values():
            if place.contains_world_point(xyz):
                self.current_area = place.name
                return

        # 3️⃣ World fallback (CRITICAL)
        self.current_area = "world"

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "target_xyz": (
                [round(v, 2) for v in self.target]
                if self.target else None
            ),
            "current_area": self.current_area,
            "speed_m_per_min": self.speed,
        }