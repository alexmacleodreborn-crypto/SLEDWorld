# world_core/walker_bot.py

import random


class WalkerBot:
    """
    Minimal world agent used ONLY to verify:
    - place membership
    - movement between places
    - world-time-driven behaviour
    """

    def __init__(self, name: str, places: dict):
        self.name = name
        self.places = places  # dict[str, WorldObject]
        self.current_place = random.choice(list(places.keys()))

        self.last_move_minute = None
        self.move_interval_minutes = 30  # moves every 30 world minutes

    # -----------------------------------------
    # WORLD TICK
    # -----------------------------------------

    def tick(self, world_clock):
        minute = world_clock.world_datetime.minute
        hour = world_clock.world_datetime.hour
        total_minutes = hour * 60 + minute

        if (
            self.last_move_minute is None
            or total_minutes - self.last_move_minute >= self.move_interval_minutes
        ):
            self.move()
            self.last_move_minute = total_minutes

    def move(self):
        self.current_place = random.choice(list(self.places.keys()))

    # -----------------------------------------
    # OBSERVER VIEW
    # -----------------------------------------

    def snapshot(self):
        return {
            "agent": self.name,
            "current_place": self.current_place,
            "movement_type": "discrete_jump",
        }