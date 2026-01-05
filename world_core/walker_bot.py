import random
import math


class WalkerBot:
    """
    Minimal world agent for validating spatial grounding.

    - Exists purely in world space (XYZ)
    - No cognition, no symbols
    - Anchored to a real position
    """

    def __init__(
        self,
        name: str,
        house,                 # HouseProfile instance
        speed: float = 1.2,    # meters per world minute
        seed: int = 42,
    ):
        self.name = name
        self.house = house
        self.speed = speed
        self.rng = random.Random(seed)

        # -----------------------------------------
        # Choose a RANDOM bedroom as anchor
        # -----------------------------------------
        bedrooms = [
            room_id for room_id, room in house.rooms.items()
            if room["type"] == "bedroom"
        ]

        chosen_room = self.rng.choice(bedrooms)

        # -----------------------------------------
        # Anchor position (XYZ)
        # -----------------------------------------
        hx, hy, hz = house.position

        # Small random offset within the house footprint
        dx = self.rng.uniform(-house.footprint[0] / 4, house.footprint[0] / 4)
        dy = self.rng.uniform(-house.footprint[1] / 4, house.footprint[1] / 4)

        self.position = [
            hx + dx,
            hy + dy,
            house.rooms[chosen_room]["z"] * 3.0,  # floor height ~3m
        ]

        self.current_room = chosen_room
        self.target = None  # XYZ target

    # -----------------------------------------
    # TARGETING
    # -----------------------------------------

    def set_target(self, position: tuple[float, float, float]):
        self.target = list(position)

    # -----------------------------------------
    # WORLD TICK
    # -----------------------------------------

    def tick(self, clock):
        """
        Move toward target using world time.
        """
        if not self.target:
            return

        # Distance vector
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dz = self.target[2] - self.position[2]

        dist = math.sqrt(dx*dx + dy*dy + dz*dz)

        if dist < 0.1:
            self.target = None
            return

        step = self.speed * clock.minutes_per_tick
        ratio = min(1.0, step / dist)

        self.position[0] += dx * ratio
        self.position[1] += dy * ratio
        self.position[2] += dz * ratio

    # -----------------------------------------
    # OBSERVER VIEW
    # -----------------------------------------

    def snapshot(self):
        return {
            "agent": self.name,
            "position_xyz": tuple(round(v, 2) for v in self.position),
            "current_room": self.current_room,
            "target_xyz": tuple(self.target) if self.target else None,
        }