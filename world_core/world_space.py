# world_core/world_space.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
import math

@dataclass
class WorldSpace:
    """
    Global environment fields (weather/light).
    Agents do not interpret as time; they just sense fields.
    """
    frame_counter: int = 0
    ambient_light: float = 0.8
    darkness: float = 0.2
    temperature: float = 0.6
    wind_active: bool = False
    rain_active: bool = False
    snow_active: bool = False

    def tick(self, frame: int) -> None:
        self.frame_counter = frame

        # gentle deterministic variation
        phase = (frame % 300) / 300.0
        self.ambient_light = 0.35 + 0.55 * (0.5 + 0.5 * math.sin(2 * math.pi * phase))
        self.darkness = max(0.0, 1.0 - self.ambient_light)
        self.temperature = 0.45 + 0.25 * (0.5 + 0.5 * math.sin(2 * math.pi * (phase + 0.25)))

        # simple toggles (rare)
        if frame % 200 == 0:
            self.wind_active = not self.wind_active
        if frame % 350 == 0:
            self.rain_active = not self.rain_active
        if frame % 500 == 0:
            self.snow_active = False  # keep off for now

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "world_space",
            "frame": self.frame_counter,
            "ambient_light": round(self.ambient_light, 3),
            "darkness": round(self.darkness, 3),
            "temperature": round(self.temperature, 3),
            "wind_active": self.wind_active,
            "rain_active": self.rain_active,
            "snow_active": self.snow_active,
        }