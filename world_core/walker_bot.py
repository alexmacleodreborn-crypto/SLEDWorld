# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical probe agent.
    - Moves
    - Can pick up remote
    - Returns to living room TV every N frames and toggles
    - Logs only physical events (no words required)
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world

        self.position = [float(start_xyz[0]), float(start_xyz[1]), float(start_xyz[2])]

        self.speed = 1.2  # meters per minute
        self.arrival_threshold = 0.5

        self.target = None
        self.target_label = None

        self.current_area = "world"
        self.heard_sound_level = 0.0

        self.ledger = []
        self._last_time = None

        self.frames = 0
        self.path = []

        # Carrying (portable objects)
        self.carrying = None  # e.g. "remote"

        # Every N frames, go to TV and toggle
        self.tv_cycle_frames = 15

        self._pick_new_target()
        self._resolve_current_area()
        self._log("initialised")

    def _log(self, event: str):
        try:
            t = self.world.clock.world_datetime.isoformat(timespec="seconds")
        except Exception:
            t = datetime.utcnow().isoformat(timespec="seconds")

        self.ledger.append({"time": t, "event": event, "area": self.current_area})

    def _get_bounds(self, obj):
        if hasattr(obj, "bounds") and obj.bounds is not None:
            return obj.bounds
        if hasattr(obj, "min_xyz") and hasattr(obj, "max_xyz"):
            return (obj.min_xyz, obj.max_xyz)
        return None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [random.uniform(min_x, max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z)]

    def _find_living_room_tv(self):
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if getattr(room, "room_type", "") == "living_room":
                        tv = getattr(room, "objects", {}).get("tv")
                        if tv and hasattr(tv, "position"):
                            return room, tv
        return None, None

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
        self._log("no_target")

    def tick(self, clock):
        self.frames += 1

        # Record path (2D view uses x,y)
        self.path.append((round(self.position[0], 2), round(self.position[1], 2), round(self.position[2], 2)))
        if len(self.path) > 500:
            self.path = self.path[-500:]

        # Every N frames: set target to TV area
        if self.frames % self.tv_cycle_frames == 0:
            room, tv = self._find_living_room_tv()
            if room and tv:
                self.target = [float(tv.position[0]), float(tv.position[1]), float(tv.position[2])]
                self.target_label = f"tv_cycle:{room.name}"
                self._log("tv_cycle_target_set")

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

    def _move(self, minutes):
        if self.target is None:
            self._pick_new_target()
            return

        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

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

    def _sense_sound(self):
        # Simple: read sound level from current room if any
        lvl = 0.0
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if room.name == self.current_area and hasattr(room, "get_sound_level"):
                    try:
                        lvl = float(room.get_sound_level())
                    except Exception:
                        lvl = 0.0
        self.heard_sound_level = round(min(lvl, 1.0), 3)

        if self.heard_sound_level >= 0.05:
            self._log(f"heard_sound:{self.heard_sound_level}")

    def _auto_interact(self):
        """
        If in living room:
        - pick up remote (if not carrying)
        - press power_toggle sometimes OR on TV cycle arrival
        """
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if room.name != self.current_area:
                    continue

                objs = getattr(room, "objects", {})
                if "remote" in objs and self.carrying is None:
                    self.carrying = "remote"
                    self._log("pickup:remote")

                # Prefer toggling during TV cycle frames or small random chance
                should_toggle = (self.frames % self.tv_cycle_frames == 0) or (random.random() < 0.03)

                if self.carrying == "remote" and should_toggle:
                    ok = room.interact("remote", "power_toggle")
                    if ok:
                        self._log("remote:power_toggle")

    def snapshot(self):
        # Distance to target
        distance = None
        if self.target:
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dz = self.target[2] - self.position[2]
            distance = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)

        return {
            "source": "walker",
            "agent": self.name,
            "frame": int(self.frames),
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "heard_sound_level": self.heard_sound_level,
            "speed_m_per_min": self.speed,
            "carrying": self.carrying,
            "path_tail": self.path[-25:],
            "ledger_tail": self.ledger[-8:],
        }