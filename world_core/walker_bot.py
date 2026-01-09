# world_core/walker_bot.py

from __future__ import annotations
import math
import random
from typing import Tuple, Optional, Dict, Any

class WalkerBot:
    """
    Physical probe. No cognition.
    - Moves around.
    - Returns to living room TV periodically and toggles via remote.
    - Wraps around neighbourhood bounds (globe/torus effect).
    """
    def __init__(
        self,
        name: str,
        start_xyz: Tuple[float, float, float],
        world_bounds,
        return_to_tv_every: int = 15,
        speed_m_per_min: float = 6.0
    ):
        self.name = name
        self.position = [float(start_xyz[0]), float(start_xyz[1]), float(start_xyz[2])]
        self.speed = float(speed_m_per_min)
        self.return_to_tv_every = int(return_to_tv_every)
        self._step_counter = 0
        self._target: Optional[Tuple[float, float, float]] = None
        self._target_label: Optional[str] = None
        self.last_action: Optional[str] = None
        self.current_area: str = "world"
        self.world_bounds = world_bounds  # ((minx,miny,minz),(maxx,maxy,maxz))

    def _wrap(self):
        if not self.world_bounds:
            return
        (minx, miny, minz), (maxx, maxy, maxz) = self.world_bounds
        # torus wrap x/y
        if self.position[0] < minx:
            self.position[0] = maxx
        elif self.position[0] > maxx:
            self.position[0] = minx
        if self.position[1] < miny:
            self.position[1] = maxy
        elif self.position[1] > maxy:
            self.position[1] = miny
        # clamp z
        self.position[2] = min(max(self.position[2], minz), maxz)

    def _pick_random_target(self, world):
        # pick a random point within neighbourhood bounds
        (minx, miny, minz), (maxx, maxy, maxz) = self.world_bounds
        self._target = (
            random.uniform(minx, maxx),
            random.uniform(miny, maxy),
            0.0
        )
        self._target_label = "wander"

    def _resolve_area(self, world):
        xyz = tuple(self.position)
        # rooms first
        for place in world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if room.contains_world_point(xyz):
                        self.current_area = room.name
                        return
        # places
        for place in world.places.values():
            if hasattr(place, "contains_world_point") and place.contains_world_point(xyz):
                self.current_area = place.name
                return
        self.current_area = "world"

    def _move_towards(self, minutes: float):
        if self._target is None:
            return
        dx = self._target[0] - self.position[0]
        dy = self._target[1] - self.position[1]
        dz = self._target[2] - self.position[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 0.5:
            self._target = None
            self._target_label = None
            return
        step = self.speed * minutes
        scale = min(step / dist, 1.0)
        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale
        self._wrap()

    def tick(self, clock, world):
        self._step_counter += 1
        self.last_action = None

        minutes = 1.0  # world.tick already steps minutes; keep simple

        # every N frames, go to house living room TV
        if self._step_counter % self.return_to_tv_every == 0:
            # find living_room tv in Family House
            tv_loc = None
            for place in world.places.values():
                if place.name == "Family House" and hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if room.room_type == "living_room":
                            tv = room.objects.get("tv")
                            if tv and hasattr(tv, "position"):
                                tv_loc = tv.position
                                # move near remote (same area)
                                self._target = (tv_loc[0], tv_loc[1] + 1.0, tv_loc[2])
                                self._target_label = "tv_return"
            if tv_loc is None and self._target is None:
                self._pick_random_target(world)

        if self._target is None:
            self._pick_random_target(world)

        self._move_towards(minutes)
        self._resolve_area(world)

        # if inside living room, attempt remote interaction
        if "living_room" in self.current_area:
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if room.name == self.current_area and "remote" in room.objects:
                            # use remote every visit
                            ok = room.interact("remote", "power_toggle")
                            if ok is not False:
                                self.last_action = "remote:power_toggle"
                            return

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "walker",
            "name": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "target": self._target_label,
            "speed_m_per_min": self.speed,
            "last_action": self.last_action,
        }