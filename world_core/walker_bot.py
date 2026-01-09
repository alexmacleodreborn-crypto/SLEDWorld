# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical actuator only.
    Periodically returns to living room TV area and uses the remote.
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

        # Frame-based behavior (no human time semantics)
        self.frame_counter = 0
        self.tv_visit_period = 15

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
        return None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        ]

    def _find_living_room_tv_point(self):
        # Search world places -> rooms -> living_room -> tv position
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if getattr(room, "room_type", "") == "living_room":
                    tv = getattr(room, "objects", {}).get("tv")
                    if tv and hasattr(tv, "position"):
                        x, y, z = tv.position
                        # Stand in front of the TV, inside the room
                        return [x, y - 1.2, z]
        return None

    def _pick_new_target(self):
        # Default wandering target: any room bounds if available, else any place bounds.
        room_targets = []
        place_targets = []
        for place in self.world.places.values():
            bounds = self._get_bounds(place)
            if bounds:
                place_targets.append((place.name, bounds))
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    rb = self._get_bounds(room)
                    if rb:
                        room_targets.append((room.name, rb))

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
        now = clock.world_datetime
        if self._last_time is None:
            self._last_time = now
            return

        self.frame_counter += 1

        delta_seconds = (now - self._last_time).total_seconds()
        self._last_time = now
        if delta_seconds <= 0:
            return

        minutes = delta_seconds / 60.0

        # Every N frames, force a visit to living room TV
        if self.frame_counter % self.tv_visit_period == 0:
            tv_point = self._find_living_room_tv_point()
            if tv_point:
                self.target = tv_point
                self.target_label = "living_room:tv_zone"
                self._log("forced_target:tv_zone")

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
            self._log(f"arrived:{self.target_label}")
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

                attenuation = 1.0 if dist < 1.0 else 1.0 / (dist ** 2)
                attenuation = max(attenuation, 0.02)
                total_sound += source * attenuation

        self.heard_sound_level = round(min(total_sound, 1.0), 3)
        if self.heard_sound_level >= 0.05:
            self._log(f"heard_sound:{self.heard_sound_level}")

    def _auto_interact(self):
        """
        If we are in the living room and close to TV zone, toggle remote.
        """
        if self.target_label != "living_room:tv_zone":
            return

        # Only toggle when we are basically at target
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]
        if math.sqrt(dx*dx + dy*dy + dz*dz) > 0.8:
            return

        # Find living room and use remote
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue
            for room in place.rooms.values():
                if getattr(room, "room_type", "") != "living_room":
                    continue
                if "remote" in getattr(room, "objects", {}):
                    room.interact("remote", "power_toggle")
                    self._log("remote:power_toggle")
                    # After interaction, wander again
                    self.target = None
                    self.target_label = None
                    return

    def snapshot(self):
        distance = None
        if self.target:
            dx = self.target[0] - self.position[0]
            dy = self.target[1] - self.position[1]
            dz = self.target[2] - self.position[2]
            distance = round(math.sqrt(dx*dx + dy*dy + dz*dz), 2)

        return {
            "source": "walker",
            "agent": self.name,
            "frame": self.frame_counter,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "heard_sound_level": self.heard_sound_level,
            "speed_m_per_min": self.speed,
            "ledger_tail": self.ledger[-5:],
        }