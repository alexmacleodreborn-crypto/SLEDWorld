import math


class WalkerBot:
    """
    Physical world walker.
    Moves through XYZ space using world time.
    Semantic location (rooms / areas) is assigned on arrival,
    never used for movement.
    """

    def __init__(self, name: str, house):
        self.name = name

        # -----------------------------------------
        # Physical state
        # -----------------------------------------
        self.position = [
            float(house.position[0]),
            float(house.position[1]),
            float(house.position[2]),
        ]  # XYZ (meters)

        self.speed = 1.2  # meters per minute (walking)

        # -----------------------------------------
        # Navigation state
        # -----------------------------------------
        self.target = None          # XYZ target
        self.arrival_threshold = 0.5  # meters

        # -----------------------------------------
        # Semantic state (observer-only)
        # -----------------------------------------
        self.current_room = 0  # semantic label ONLY

        # -----------------------------------------
        # Time anchor
        # -----------------------------------------
        self._last_time = None  # datetime of last tick

    # =================================================
    # NAVIGATION
    # =================================================

    def set_target(self, xyz):
        """
        Set a new physical destination.
        xyz must be a 3-element iterable.
        """
        self.target = [
            float(xyz[0]),
            float(xyz[1]),
            float(xyz[2]),
        ]

    # =================================================
    # WORLD TICK
    # =================================================

    def tick(self, clock):
        """
        Advances the bot using world time.
        """
        if self.target is None:
            return

        now = clock.world_datetime

        # Initialise time anchor
        if self._last_time is None:
            self._last_time = now
            return

        delta_seconds = (now - self._last_time).total_seconds()
        self._last_time = now

        if delta_seconds <= 0:
            return

        minutes = delta_seconds / 60.0
        self._move_towards_target(minutes)

    def _move_towards_target(self, minutes):
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]

        # Z is NOT interpolated for walking
        dz = 0.0

        distance = math.sqrt(dx * dx + dy * dy)

        # -----------------------------------------
        # Arrival check
        # -----------------------------------------
        if distance <= self.arrival_threshold:
            self._on_arrival()
            return

        step = self.speed * minutes
        scale = min(step / distance, 1.0)

        self.position[0] += dx * scale
        self.position[1] += dy * scale
        # Z unchanged (ground walking)

    def _on_arrival(self):
        """
        Called once the target is reached.
        Semantic updates belong here.
        """
        self.target = None
        # current_room / area can be updated later

    # =================================================
    # OBSERVER VIEW
    # =================================================

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
            "speed_m_per_min": self.speed,
        }