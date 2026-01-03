import math

class WorldCycles:
    """
    Continuous physical cycles.
    No symbols, no labels.
    """

    def __init__(self, day_length_hours: float = 24.0):
        self.day_length = day_length_hours

    def sample(self, world_hours: float) -> dict:
        """
        Returns raw physical signals.
        """
        phase = (world_hours % self.day_length) / self.day_length
        angle = 2 * math.pi * phase

        # Smooth oscillations
        light = max(0.0, math.sin(angle))
        heat = max(0.0, math.sin(angle + math.pi / 6))

        return {
            "light": round(light, 3),
            "heat": round(heat, 3),
        }