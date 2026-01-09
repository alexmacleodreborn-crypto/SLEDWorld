# world_core/world_space.py

from dataclasses import dataclass, asdict
import math
import random


@dataclass
class WeatherState:
    ambient_light: float = 0.6   # 0..1
    darkness: float = 0.2        # 0..1
    temperature_c: float = 12.0
    wind_level: float = 0.2      # 0..1
    rain: bool = False
    snow: bool = False
    cloud: float = 0.2           # 0..1


class WorldSpace:
    """
    Global world fields (weather / sky).
    - No clock exposed
    - Evolves per world frame
    - Agents perceive fields, not "time"
    """

    def __init__(self, seed: int = 211, frames_per_cycle: int = 240):
        self.rng = random.Random(seed)
        self.frames_per_cycle = max(60, int(frames_per_cycle))
        self.frame_counter = 0
        self.state = WeatherState()

        self._rain_left = 0
        self._snow_left = 0
        self._wind_left = 0

    def _phase(self) -> float:
        return (self.frame_counter % self.frames_per_cycle) / float(self.frames_per_cycle)

    def tick(self):
        self.frame_counter += 1
        phase = self._phase()

        # Base daylight curve (sinusoid)
        base_light = 0.5 + 0.5 * math.sin(2 * math.pi * (phase - 0.25))
        base_light = max(0.0, min(1.0, base_light))

        # Cloud drift
        cloud = self.state.cloud + self.rng.uniform(-0.05, 0.05)
        cloud = max(0.0, min(1.0, cloud))

        # Clouds reduce effective light
        eff_light = base_light * (1.0 - 0.6 * cloud)
        eff_light = max(0.0, min(1.0, eff_light))

        # Wind bursts
        if self._wind_left > 0:
            self._wind_left -= 1
        else:
            if self.rng.random() < 0.06:
                self._wind_left = self.rng.randint(10, 40)

        wind = 0.15 + (0.35 if self._wind_left > 0 else 0.0) + self.rng.uniform(-0.05, 0.05)
        wind = max(0.0, min(1.0, wind))

        # Temp follows light
        temp = 10.0 + 10.0 * (eff_light - 0.5)

        # Precip events
        if self._rain_left > 0:
            self._rain_left -= 1
        if self._snow_left > 0:
            self._snow_left -= 1

        if self._rain_left == 0 and self._snow_left == 0:
            if cloud > 0.55 and self.rng.random() < 0.05:
                if temp <= 1.0 and self.rng.random() < 0.45:
                    self._snow_left = self.rng.randint(20, 60)
                else:
                    self._rain_left = self.rng.randint(20, 60)

        rain = self._rain_left > 0
        snow = self._snow_left > 0
        if rain:
            temp -= 1.5
        if snow:
            temp -= 3.0

        darkness = (1.0 - eff_light) * (0.7 + 0.3 * cloud)
        darkness = max(0.0, min(1.0, darkness))

        self.state.ambient_light = round(eff_light, 3)
        self.state.cloud = round(cloud, 3)
        self.state.wind_level = round(wind, 3)
        self.state.temperature_c = round(temp, 2)
        self.state.rain = bool(rain)
        self.state.snow = bool(snow)
        self.state.darkness = round(darkness, 3)

    def snapshot(self) -> dict:
        d = asdict(self.state)
        d.update({
            "source": "world_space",
            "frame": int(self.frame_counter),
            "cycle_hint": round(self._phase(), 3),  # coordinate-like phase, not "time"
        })
        return d