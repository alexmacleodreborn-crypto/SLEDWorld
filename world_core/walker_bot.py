# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical causal agent.

    Rules:
    - Moves continuously in world space
    - No cognition
    - No learning
    - Causes physical state changes only
    - Time is external (via WorldClock)
    """

    def __init__(
        self,
        name: str,
        start_xyz,
        world,
        speed_m_per_min: float = 1.2,
        arrival_threshold: float = 0.5,
        return_interval: int = 15,
    ):
        self.name = name
        self.world = world

        # -----------------------------------------
        # Physical state
        # -----------------------------------------
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]

        self.speed = float(speed_m_per_min)
        self.arrival_threshold = float(arrival_threshold)

        # -----------------------------------------
        # Navigation
        # -----------------------------------------
        self.target = None
        self.target_label = None
        self.return_interval = int(return_interval)

        # -----------------------------------------
        # Semantic location (non-cognitive)
        # -----------------------------------------
        self.current_area = "world"

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None
        self._frame_counter = 0

        # Bootstrap
        self._pick_new_target()
        self._resolve_current_area()

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
        self._frame_counter += 1

        self._move(minutes)
        self._resolve_current_area()
        self._auto_interact()

    # =================================================
    # MOVEMENT
    # =================================================

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
    # LOCATION RESOLUTION (RESTORED)
    # =================================================

    def _resolve_current_area(self):
        """
        Determine which room or place the walker is currently in.
        """

        xyz = tuple(self.position)

        # Rooms first (most specific)
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return

        # Then places
        for place in self.world.places.values():
            if hasattr(place, "contains_world_point"):
                if place.contains_world_point(xyz):
                    self.current_area = place.name
                    return

        self.current_area = "world"

    # =================================================
    # TARGET SELECTION
    # =================================================

    def _pick_new_target(self):
        """
        Choose a random navigable point in the world.
        """

        room_targets = []
        place_targets = []

        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if hasattr(room, "bounds"):
                        room_targets.append((room.name, room.bounds))

            if hasattr(place, "bounds"):
                place_targets.append((place.name, place.bounds))

        if room_targets:
            label, bounds = random.choice(room_targets)
            self.target = self._random_point_in_bounds(bounds)
            self.target_label = label
            return

        if place_targets:
            label, bounds = random.choice(place_targets)
            self.target = self._random_point_in_bounds(bounds)
            self.target_label = label
            return

        self.target = None
        self.target_label = None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        ]

    # =================================================
    # PHYSICAL INTERACTION
    # =================================================

    def _auto_interact(self):
        """
        Periodically interact with room objects (e.g. TV).
        """

        if self._frame_counter % self.return_interval != 0:
            return

        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if room.name != self.current_area:
                    continue

                if "remote" in room.objects:
                    room.interact("remote", "power_toggle")
                    return

    # =================================================
    # OBSERVER SNAPSHOT
    # =================================================

    def snapshot(self):
        distance = None
        if self.target:
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dz = self.target[2] - self.position[2]
            distance = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)

        return {
            "source": "walker",
            "name": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "speed_m_per_min": self.speed,
        }