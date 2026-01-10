# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical probe agent.

    Purpose:
    - Move through world geometry using world time
    - Trigger real interactions (TV remote)
    - Provide grounded sensory telemetry (position, area, heard_sound)

    Rules:
    - No cognition
    - No learning
    - Motion is continuous in XYZ
    """

    def __init__(
        self,
        name: str,
        start_xyz,
        world,
        speed_m_per_min: float = 1.2,
        arrival_threshold_m: float = 0.5,
        return_interval: int = 15,  # return to living room and toggle TV
    ):
        self.name = name
        self.world = world

        # Physical state
        self.position = [float(start_xyz[0]), float(start_xyz[1]), float(start_xyz[2])]
        self.speed = float(speed_m_per_min)
        self.arrival_threshold = float(arrival_threshold_m)

        # Navigation
        self.target = None
        self.target_label = None

        # Semantic/sensory
        self.current_area = "world"
        self.heard_sound_level = 0.0

        # Frame-based routine
        self.return_interval = int(return_interval)
        self._last_toggle_frame = None
        self._forced_target = None  # living_room target when routine triggers

        # Logging
        self.ledger = []

        # Time anchor
        self._last_time = None

        # Bootstrap
        self._pick_new_target()
        self._resolve_current_area()
        self._log("initialised")

    # =================================================
    # Logging
    # =================================================

    def _log(self, event: str, extra: dict | None = None):
        try:
            t = self.world.clock.world_datetime.isoformat(timespec="seconds")
        except Exception:
            t = datetime.utcnow().isoformat(timespec="seconds")

        rec = {
            "time": t,
            "event": event,
            "area": self.current_area,
            "pos": [round(v, 2) for v in self.position],
            "frame": getattr(self.world, "frame", None),
        }
        if extra:
            rec.update(extra)
        self.ledger.append(rec)

    # =================================================
    # Helpers
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

    def _find_living_room_target(self):
        """
        Find a stable point inside a living_room if present.
        Used for the return_interval routine (TV toggle).
        """
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if getattr(room, "room_type", "") == "living_room":
                    bounds = self._get_bounds(room)
                    if bounds:
                        return ("living_room", self._random_point_in_bounds(bounds), room)
        return (None, None, None)

    def _pick_new_target(self):
        room_targets = []
        place_targets = []

        for place in self.world.places.values():
            # Rooms
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    bounds = self._get_bounds(room)
                    if bounds:
                        room_targets.append((room.name, bounds))

            # Place bounds
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

    # =================================================
    # Main tick
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

        # minutes of world time
        minutes = delta_seconds / 60.0

        # Frame-based routine: every N frames, go to living_room and toggle TV
        wf = getattr(self.world, "frame", 0)
        if self.return_interval > 0:
            if self._last_toggle_frame is None:
                self._last_toggle_frame = wf
            if (wf - self._last_toggle_frame) >= self.return_interval:
                label, target, room = self._find_living_room_target()
                if target is not None:
                    self._forced_target = ("living_room", target, room)
                    self.target = target
                    self.target_label = "living_room"
                    self._log("routine:return_to_living_room")
                self._last_toggle_frame = wf

        # Move
        self._move(minutes)

        # Resolve semantics + sense
        self._resolve_current_area()
        self._sense_sound()

        # If we reached routine room, interact with TV
        self._auto_interact_tv()

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
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        if distance <= self.arrival_threshold:
            self._log(f"arrived:{self.target_label or self.current_area}")
            # If we arrived at a forced (routine) target, keep target until interaction clears it
            if self._forced_target is None:
                self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # Semantic resolution (safe)
    # =================================================

    def _resolve_current_area(self):
        xyz = tuple(self.position)

        # Rooms first
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    try:
                        if hasattr(room, "contains_world_point") and room.contains_world_point(xyz):
                            self.current_area = room.name
                            return
                    except Exception:
                        continue

        # Then places
        for place in self.world.places.values():
            try:
                if hasattr(place, "contains_world_point") and place.contains_world_point(xyz):
                    self.current_area = place.name
                    return
            except Exception:
                continue

        self.current_area = "world"

    # =================================================
    # Sensing (sound)
    # =================================================

    def _sense_sound(self):
        total_sound = 0.0
        x, y, z = self.position

        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                # prefer room.get_sound_level()
                source = 0.0
                if hasattr(room, "get_sound_level"):
                    try:
                        source = float(room.get_sound_level())
                    except Exception:
                        source = 0.0

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
                dist = math.sqrt(dx * dx + dy * dy + dz * dz)

                attenuation = 1.0 if dist < 1.0 else 1.0 / (dist ** 2)
                attenuation = max(attenuation, 0.02)
                total_sound += source * attenuation

        self.heard_sound_level = round(min(total_sound, 1.0), 3)

        if self.heard_sound_level >= 0.05:
            self._log("heard_sound", {"heard_sound_level": self.heard_sound_level})

    # =================================================
    # Interaction (TV toggle when in living room)
    # =================================================

    def _auto_interact_tv(self):
        """
        If we are in the living room and it has a remote,
        toggle TV when we arrived due to routine.
        """
        if self._forced_target is None:
            return

        forced_label, _, forced_room = self._forced_target

        # Must be inside the forced room area now
        if forced_room is None or self.current_area != forced_room.name:
            return

        # Use remote to toggle TV if available
        try:
            if hasattr(forced_room, "objects") and "remote" in forced_room.objects:
                forced_room.interact("remote", "power_toggle")
                self._log("remote:power_toggle")
        except Exception:
            self._log("remote:power_toggle_failed")

        # Clear forced state and pick new random target
        self._forced_target = None
        self._pick_new_target()

    # =================================================
    # Snapshot (for streamlit + ledger)
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
            "agent": self.name,
            "frame": getattr(self.world, "frame", None),
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "heard_sound_level": self.heard_sound_level,
            "speed_m_per_min": self.speed,
            "ledger_tail": self.ledger[-5:],
        }