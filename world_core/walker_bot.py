# world_core/walker_bot.py

import math


class WalkerBot:
    """
    Physical world walker.
    Moves through XYZ space using world time.
    """

    def __init__(self, name: str, house):
        self.name = name

        # Start at house position
        self.position = list(house.position)  # [x, y, z]
        self.current_room = 0

        self.target = None
        self.speed = 1.2  # meters per minute (walking)

        self._last_time = None  # world_datetime anchor

    # -----------------------------------------
    # Navigation
    # -----------------------------------------

    def set_target(self, xyz):
        self.target = list(xyz)

    # -----------------------------------------
    # WORLD TICK
    # -----------------------------------------

    def tick(self, clock):
        if self.target is None:
            return

        # --- time delta (minutes) ---
        now = clock.world_datetime
        if self._last_time is None:
            self._last_time = now
            return

        delta_seconds = (now - self._last_time).total_seconds()
        self._last_time = now

        minutes = delta_seconds / 60.0
        if minutes <= 0:
            return

        # --- movement ---
        self._move_towards_target(minutes)

    def _move_towards_target(self, minutes):
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        if distance < 0.5:
            return  # arrived

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale  # see Z fix below

    # -----------------------------------------
    # OBSERVER VIEW
    # -----------------------------------------

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": [
                round(self.position[0], 2),
                round(self.position[1], 2),
                round(self.position[2], 2),
            ],
            "target_xyz": self.target,
            "current_room": self.current_room,
        }