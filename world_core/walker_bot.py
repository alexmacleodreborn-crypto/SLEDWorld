import math
import random
from datetime import datetime


class WalkerBot:
    """
    Pure physical actor.
    No cognition. No learning.
    Generates repeatable causal structure for observers.
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world

        # Physical state
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]

        self.speed = 1.2  # meters per minute
        self.arrival_threshold = 0.5

        # Navigation
        self.target = None
        self.target_label = None

        # Semantic / sensory
        self.current_area = "world"
        self.heard_sound_level = 0.0

        # Ledger (observer-visible)
        self.ledger = []

        # Time anchor
        self._last_time = None

        # Deterministic TV behaviour
        self.frame_counter = 0
        self.tv_cycle = 15

        # Bootstrap
        self._pick_new_target()
        self._resolve_current_area()
        self._log("initialised")

    # =================================================
    # Logging
    # =================================================

    def _log(self, event: str):
        try:
            t = self.world.clock.world_datetime.isoformat(timespec="seconds")
        except Exception:
            t = datetime.utcnow().isoformat(timespec="seconds")

        self.ledger.append({
            "time": t,
            "event": event,
            "area": self.current_area,
        })

    # =================================================
    # Geometry helpers
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
    # Target selection
    # =================================================

    def _pick_new_target(self):
        place_targets = []

        for place in self.world.places.values():
            bounds = self._get_bounds(place)
            if bounds:
                place_targets.append((place.name, bounds))

        if place_targets:
            label, bounds = random.choice(place_targets)
            self.target = self._random_point_in_bounds(bounds)
            self.target_label = label
            self._log(f"new_target:{label}")
            return

        self.target = None
        self.target_label = None
        self._log("no_target")

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

        self.frame_counter += 1
        minutes = delta_seconds / 60.0

        # Deterministic TV cycle
        if self.frame_counter % self.tv_cycle == 0:
            self._force_tv_interaction()

        self._move(minutes)
        self._resolve_current_area()
        self._sense_sound()

    # =================================================
    # Forced TV interaction
    # =================================================

    def _force_tv_interaction(self):
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if "tv" in getattr(room, "objects", {}):
                    bounds = self._get_bounds(room)
                    if bounds:
                        self.target = self._random_point_in_bounds(bounds)
                        self.target_label = room.name

                    if self.current_area == room.name:
                        room.interact("tv", "power_toggle")
                        self._log("tv:power_toggle")

                    return

    # =================================================
    # Movement
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
            self._log(f"arrived:{self.current_area}")
            self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # Area resolution
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
    # Sound sensing
    # =================================================

    def _sense_sound(self):
        total_sound = 0.0
        x, y, z = self.position

        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if not hasattr(room, "get_sound_level"):
                    continue

                source = room.get_sound_level()
                if source <= 0:
                    continue

                bounds = self._get_bounds(room)
                if not bounds:
                    continue

                (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
                cx = (min_x + max_x) / 2
                cy = (min_y + max_y) / 2
                cz = (min_z + max_z) / 2

                dx = x - cx
                dy = y - cy
                dz = z - cz
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                attenuation = 1.0 if dist < 1 else max(1.0 / (dist**2), 0.02)
                total_sound += source * attenuation

        self.heard_sound_level = round(min(total_sound, 1.0), 3)

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        return {
            "source": "walker",
            "name": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "heard_sound_level": self.heard_sound_level,
            "frame": self.frame_counter,
            "ledger_tail": self.ledger[-5:],
        }