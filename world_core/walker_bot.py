# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Pure physical agent.

    - Walks the world
    - Returns to TV at fixed intervals
    - Toggles TV power (on/off)
    - No learning
    - No cognition
    """

    def __init__(
        self,
        name: str,
        start_xyz,
        world,
        speed_m_per_min: float = 1.2,
        return_interval: int = 15,
    ):
        self.name = name
        self.world = world

        # -----------------------------
        # Physical state
        # -----------------------------
        self.position = [
            float(start_xyz[0]),
            float(start_xyz[1]),
            float(start_xyz[2]),
        ]

        self.speed = float(speed_m_per_min)
        self.arrival_threshold = 0.5

        # -----------------------------
        # Behaviour control
        # -----------------------------
        self.return_interval = int(return_interval)
        self.frame_counter = 0

        self.target = None
        self.target_label = None

        # -----------------------------
        # Observer-visible state
        # -----------------------------
        self.current_area = "world"
        self.ledger = []

        self._last_time = None

        self._pick_new_target()
        self._log("initialised")

    # =================================================
    # Logging (world time)
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
    # Targeting
    # =================================================

    def _pick_new_target(self):
        """
        Random wander target.
        """
        places = list(self.world.places.values())
        if not places:
            return

        place = random.choice(places)

        if hasattr(place, "random_point_inside"):
            self.target = list(place.random_point_inside())
            self.target_label = place.name
        else:
            self.target = list(place.position)
            self.target_label = place.name

    def _target_tv(self):
        """
        Force target to TV location.
        """
        for place in self.world.places.values():
            if hasattr(place, "rooms"):
                for room in place.rooms.values():
                    if "tv" in room.objects:
                        tv = room.objects["tv"]
                        self.target = list(tv.position)
                        self.target_label = "tv"
                        return

    # =================================================
    # World tick
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

        self.frame_counter += 1

        # Every N frames → return to TV
        if self.frame_counter % self.return_interval == 0:
            self._target_tv()

        self._move(minutes)
        self._resolve_current_area()
        self._interact_if_possible()

    # =================================================
    # Movement
    # =================================================

    def _move(self, minutes):
        if not self.target:
            self._pick_new_target()
            return

        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if distance <= self.arrival_threshold:
            self._log(f"arrived:{self.target_label}")
            self._pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # =================================================
    # Interaction
    # =================================================

    def _interact_if_possible(self):
        """
        Toggle TV if inside living room.
        """
        for place in self.world.places.values():
            if not hasattr(place, "rooms"):
                continue

            for room in place.rooms.values():
                if room.contains_world_point(tuple(self.position)):
                    self.current_area = room.name

                    if "remote" in room.objects:
                        room.interact("remote", "power_toggle")
                        self._log("tv:power_toggle")
                        return

    # =================================================
    # Observer snapshot
    # =================================================

    def snapshot(self):
        return {
            "source": "walker",
            "name": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_area": self.current_area,
            "target": self.target_label,
            "frame": self.frame_counter,
            "ledger_tail": self.ledger[-5:],
        }