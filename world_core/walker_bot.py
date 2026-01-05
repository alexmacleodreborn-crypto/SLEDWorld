import math
import random


class WalkerBot:
    """
    Physical world walker.
    Moves continuously in XYZ and occupies real rooms.
    """

    def __init__(self, name: str, house):
        self.name = name
        self.house = house

        # Start in random bedroom
        self.current_room = random.choice([3, 4])
        self.position = list(house.random_point_in_room(self.current_room))

        self.target = None
        self.speed = 1.2  # meters per minute
        self._last_time = None

        # Pick initial target
        self.pick_new_target()

    # ---------------------------------
    # Behaviour
    # ---------------------------------

    def pick_new_target(self):
        self.current_room = random.choice(list(self.house.rooms.keys()))
        self.target = list(self.house.random_point_in_room(self.current_room))

    # ---------------------------------
    # WORLD TICK
    # ---------------------------------

    def tick(self, clock):
        now = clock.world_datetime

        if self._last_time is None:
            self._last_time = now
            return

        delta_minutes = (now - self._last_time).total_seconds() / 60.0
        self._last_time = now

        if delta_minutes <= 0:
            return

        self._move(delta_minutes)

    def _move(self, minutes):
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if distance < 0.5:
            self.pick_new_target()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        self.position[2] += dz * scale

    # ---------------------------------
    # OBSERVER VIEW
    # ---------------------------------

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": [round(v, 2) for v in self.position],
            "current_room": self.current_room,
            "target_xyz": [round(v, 2) for v in self.target],
            "speed_m_per_min": self.speed,
        }