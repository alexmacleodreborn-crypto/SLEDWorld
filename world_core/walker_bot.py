# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Ghost / probe agent.

    Purpose:
    - Validate world geometry
    - Validate time scaling
    - Validate sound propagation (INCLUDING BLEED)
    - Validate interaction affordances

    Rules:
    - Moves continuously in XYZ using world time
    - NEVER stops
    - Semantic location is ALWAYS defined
    - No cognition
    - No learning
    """

    def __init__(self, name: str, start_xyz, world):
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

        self.speed = 1.2  # m/min
        self.arrival_threshold = 0.5

        # -----------------------------------------
        # Navigation
        # -----------------------------------------
        self.target = None
        self.target_label = None

        # -----------------------------------------
        # Semantic + sensory state
        # -----------------------------------------
        self.current_area = "world"
        self.heard_sound_level = 0.0

        # -----------------------------------------
        # Observer ledger
        # -----------------------------------------
        self.ledger = []

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None

        # Bootstrap
        self._pick_new_target()
        self._resolve_current_area()
        self._log("initialised")

    # =================================================
    # INTERNAL LOGGING
    # =================================================

    def _log(self, event: str):
        self.ledger.append({
            "time": datetime.utcnow().isoformat(timespec="seconds"),
            "event": event,
            "area": self.current_area,
        })

    # =================================================
    # GEOMETRY HELPERS
    # =================================================

    def _get_bounds(self, obj):
        if hasattr(obj, "bounds") and obj.bounds is not None:
            return obj.bounds
        if hasattr(obj, "min_xyz") and hasattr(obj, "max_xyz"):
            return (obj.min_xyz, obj.max_xyz)
        return None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        ]

    # =================================================
    # TARGET SELECTION
    # =================================================

    def _pick_new_target(self):
        room_targets = []
        place_targets = []

        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    bounds = self._get_bounds(room)
                    if bounds:
                        room_targets.append((room.name, bounds))

            bounds = self._get_bounds(place)
            if bounds:
                place_targets.append((place.name, bounds))

        if room_targets:
            label, bounds = random.choice(room_targets)
            self.target = self._random_point_in_bounds(bounds)
            self.target_label = label
            self._log(f"new_target_room:{label}")
            return

        if place_targets:
            label, bounds = random.choice(place_targets)
            self.target = self._random_point_in_bounds(bounds)
            self.target_label = label
            self._log(f"new_target_place:{label}")
            return

        self.target = None
        self.target_label = None

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
        self._sense_sound()
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

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if distance <= self.arrival_threshold:
            self._resolve_current_area()
            self._log(f"arrived:{self.current_area}")
            self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # SEMANTIC RESOLUTION
    # =================================================

    def _resolve_current_area(self):
        xyz = tuple(self.position)

        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return

        for place in self.world.places.values():
            if place.contains_world_point(xyz):
                self.current_area = place.name
                return

        self.current_area = "world"

    # =================================================
    # SENSING (SOUND WITH BLEED)
    # =================================================

    def _sense_sound(self):
        """
        Hear sound from ALL rooms with distance attenuation.
        """
        total_sound = 0.0
        x, y, z = self.position

        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():

                    if not hasattr(room, "get_sound_level"):
                        continue

                    source_level = room.get_sound_level()
                    if source_level <= 0:
                        continue

                    # Room center
                    (min_x, min_y, min_z), (max_x, max_y, max_z) = room.bounds
                    cx = (min_x + max_x) / 2
                    cy = (min_y + max_y) / 2
                    cz = (min_z + max_z) / 2

                    dx = x - cx
                    dy = y - cy
                    dz = z - cz
                    distance = math.sqrt(dx*dx + dy*dy + dz*dz)

                    # Attenuation model
                    if distance < 1.0:
                        attenuation = 1.0
                    else:
                        attenuation = 1.0 / (distance ** 2)

                    total_sound += source_level * attenuation

        self.heard_sound_level = round(min(total_sound, 1.0), 3)

        if self.heard_sound_level > 0:
            self._log(f"heard_sound:{self.heard_sound_level}")

    # =================================================
    # PHYSICAL INTERACTION (DEMO)
    # =================================================

    def _auto_interact(self):
        """
        Ghost behaviour:
        - Occasionally toggles or adjusts TV in living room
        """
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.name == self.current_area and "tv" in getattr(room, "objects", {}):
                        if random.random() < 0.02:
                            room.interact("tv", "power_toggle")
                            self._log("tv:power_toggle")
                        elif random.random() < 0.05:
                            room.interact("tv", "volume_up")
                            self._log("tv:volume_up")

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        distance = None
        if self.target:
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dz = self.target[2] - self.position[2]
            distance = round(math.sqrt(dx*dx + dy*dy + dz*dz), 2)

        return {
            "agent": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "heard_sound_level": self.heard_sound_level,
            "speed_m_per_min": self.speed,
            "ledger_tail": self.ledger[-5:],
        }