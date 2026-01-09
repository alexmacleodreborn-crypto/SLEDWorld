# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical probe agent.
    Moves using world time.
    Interacts with objects when in proximity.

    Update:
      - Every N frames, returns to living-room TV and toggles power.
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
        self._frame_counter = 0
        self._tv_return_period = 15  # frames
        self._force_tv_mode = True

        self._pick_new_target()
        self._resolve_current_area()
        self._log("initialised")

    def _log(self, event: str):
        try:
            t = self.world.clock.world_datetime.isoformat(timespec="seconds")
        except Exception:
            t = datetime.utcnow().isoformat(timespec="seconds")

        self.ledger.append({
            "time": t,
            "frame": self._frame_counter,
            "event": event,
            "area": self.current_area,
        })

    def _get_bounds(self, obj):
        b = getattr(obj, "bounds", None)
        if b is not None:
            return b
        min_xyz = getattr(obj, "min_xyz", None)
        max_xyz = getattr(obj, "max_xyz", None)
        if min_xyz and max_xyz:
            return (min_xyz, max_xyz)
        return None

    def _random_point_in_bounds(self, bounds):
        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
        return [
            random.uniform(min_x, max_x),
            random.uniform(min_y, max_y),
            random.uniform(min_z, max_z),
        ]

    def _find_living_room_tv_point(self):
        # Find a living_room and return the TV position if possible
        for place in self.world.places.values():
            rooms = getattr(place, "rooms", None)
            if not rooms:
                continue
            for room in rooms.values():
                if getattr(room, "room_type", "") == "living_room":
                    objs = getattr(room, "objects", {})
                    tv = objs.get("tv")
                    if tv and hasattr(tv, "position"):
                        return list(tv.position), f"{room.name}:tv"
                    # fallback: center of room
                    bounds = self._get_bounds(room)
                    if bounds:
                        (min_x, min_y, min_z), (max_x, max_y, max_z) = bounds
                        return [(min_x+max_x)/2, (min_y+max_y)/2, (min_z+max_z)/2], room.name
        return None, None

    def _pick_new_target(self):
        # Periodic forced return to TV
        if self._force_tv_mode and (self._frame_counter % self._tv_return_period == 0):
            tv_pt, label = self._find_living_room_tv_point()
            if tv_pt is not None:
                self.target = tv_pt
                self.target_label = label
                self._log(f"force_target:{label}")
                return

        room_targets = []
        place_targets = []

        for place in self.world.places.values():
            rooms = getattr(place, "rooms", None)
            if rooms:
                for room in rooms.values():
                    bounds = self._get_bounds(room)
                    if bounds:
                        room_targets.append((getattr(room, "name", "room"), bounds))

            bounds = self._get_bounds(place)
            if bounds:
                place_targets.append((getattr(place, "name", "place"), bounds))

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
        self._frame_counter += 1
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
        self._auto_interact()

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

            # If arrived at TV target: toggle TV using remote if possible
            if self.target_label and ":tv" in self.target_label:
                self._try_toggle_tv()
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
            rooms = getattr(place, "rooms", None)
            if rooms:
                for room in rooms.values():
                    if hasattr(room, "contains_world_point") and room.contains_world_point(xyz):
                        self.current_area = getattr(room, "name", "room")
                        return
        for place in self.world.places.values():
            if hasattr(place, "contains_world_point") and place.contains_world_point(xyz):
                self.current_area = getattr(place, "name", "place")
                return
        self.current_area = "world"

    def _try_toggle_tv(self):
        # Try to find current room and use remote to toggle tv
        for place in self.world.places.values():
            rooms = getattr(place, "rooms", None)
            if not rooms:
                continue
            for room in rooms.values():
                if getattr(room, "name", "") != self.current_area:
                    continue
                objs = getattr(room, "objects", {})
                if "remote" in objs:
                    try:
                        room.interact("remote", "power_toggle")
                        self._log("remote:power_toggle")
                        return
                    except Exception:
                        pass
                if "tv" in objs:
                    tv = objs["tv"]
                    if hasattr(tv, "power_toggle"):
                        tv.power_toggle()
                        self._log("tv:power_toggle_direct")
                        return

    def _auto_interact(self):
        # Optional extra random actions if in the living room
        for place in self.world.places.values():
            rooms = getattr(place, "rooms", None)
            if not rooms:
                continue
            for room in rooms.values():
                if getattr(room, "name", "") != self.current_area:
                    continue
                objs = getattr(room, "objects", {})
                if "remote" not in objs:
                    return
                r = random.random()
                if r < 0.01:
                    room.interact("remote", "power_toggle")
                    self._log("remote:power_toggle_random")
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
            "type": "walker",
            "name": self.name,
            "frame": self._frame_counter,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "destination": self.target_label,
            "distance_to_target_m": distance,
            "speed_m_per_min": self.speed,
            "ledger_tail": self.ledger[-10:],
        }