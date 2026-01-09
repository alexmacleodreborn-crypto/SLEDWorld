# world_core/world_space.py

from __future__ import annotations
import math
import random
from dataclasses import dataclass, asdict


@dataclass
class WeatherState:
    # Global “sky fields” (no clock exposed)
    ambient_light: float = 0.6     # 0..1
    temperature_c: float = 12.0    # simple global temp
    wind_level: float = 0.2        # 0..1
    rain: bool = False
    snow: bool = False
    cloud: float = 0.2             # 0..1
    darkness: float = 0.2          # 0..1 (inverse-ish of light, but can differ due to cloud)


class WorldSpace:
    """
    Global atmosphere/sky layer.
    - Day-like cycle but NEVER exposes "time"
    - Outputs only fields: light, temp, wind, precipitation

    Internals:
    - frame_counter advances each world.tick()
    - cycle_phase is derived from frame_counter (but not presented as time)
    """

    def __init__(
        self,
        seed: int = 211,
        frames_per_cycle: int = 240,   # “one earth day” mapped to frames (not time)
        base_temp_c: float = 12.0,
        temp_swing_c: float = 6.0,
    ):
        self.rng = random.Random(seed)
        self.frames_per_cycle = max(60, int(frames_per_cycle))
        self.base_temp_c = float(base_temp_c)
        self.temp_swing_c = float(temp_swing_c)

        self.frame_counter = 0
        self.state = WeatherState()

        # event persistence counters (no “time”, just steps)
        self._rain_steps_left = 0
        self._snow_steps_left = 0
        self._wind_steps_left = 0

    def _cycle_phase(self) -> float:
        # 0..1 repeating
        return (self.frame_counter % self.frames_per_cycle) / float(self.frames_per_cycle)

    def tick(self):
        """
        Advance global fields by 1 world frame.
        """
        self.frame_counter += 1
        phase = self._cycle_phase()  # 0..1

        # -------------------------
        # Day-like ambient light curve
        # (sinusoid: bright mid-cycle, dark at phase~0)
        # -------------------------
        # shift so “night” roughly near phase 0, “day” near 0.5
        light = 0.5 + 0.5 * math.sin(2 * math.pi * (phase - 0.25))
        light = max(0.0, min(1.0, light))

        # clouds reduce light
        # cloud drifts slowly
        cloud = self.state.cloud + self.rng.uniform(-0.05, 0.05)
        cloud = max(0.0, min(1.0, cloud))
        light_eff = light * (1.0 - 0.6 * cloud)

        # -------------------------
        # Temperature follows light (simple)
        # -------------------------
        temp = self.base_temp_c + self.temp_swing_c * (light - 0.5) * 2.0
        # precipitation lowers temp a bit
        if self.state.rain:
            temp -= 1.5
        if self.state.snow:
            temp -= 3.0

        # -------------------------
        # Wind bursts (toggle-ish)
        # -------------------------
        if self._wind_steps_left > 0:
            self._wind_steps_left -= 1
        else:
            # small chance to start wind burst
            if self.rng.random() < 0.06:
                self._wind_steps_left = self.rng.randint(10, 40)

        wind = 0.15 + 0.35 * (1.0 if self._wind_steps_left > 0 else 0.0)
        wind += self.rng.uniform(-0.05, 0.05)
        wind = max(0.0, min(1.0, wind))

        # -------------------------
        # Rain / Snow toggles
        # -------------------------
        # Rain chance rises with cloud; snow chance rises if cold
        if self._rain_steps_left > 0:
            self._rain_steps_left -= 1
        if self._snow_steps_left > 0:
            self._snow_steps_left -= 1

        # trigger events
        if self._rain_steps_left == 0 and self._snow_steps_left == 0:
            if cloud > 0.55 and self.rng.random() < 0.05:
                if temp <= 1.0 and self.rng.random() < 0.45:
                    self._snow_steps_left = self.rng.randint(20, 60)
                else:
                    self._rain_steps_left = self.rng.randint(20, 60)

        rain = self._rain_steps_left > 0
        snow = self._snow_steps_left > 0

        # darkness is not "night" explicitly; it’s a field
        darkness = (1.0 - light_eff) * (0.7 + 0.3 * cloud)
        darkness = max(0.0, min(1.0, darkness))

        self.state.ambient_light = round(light_eff, 3)
        self.state.cloud = round(cloud, 3)
        self.state.temperature_c = round(temp, 2)
        self.state.wind_level = round(wind, 3)
        self.state.rain = bool(rain)
        self.state.snow = bool(snow)
        self.state.darkness = round(darkness, 3)

    def snapshot(self) -> dict:
        # No clock fields. Only environment fields + frame.
        base = asdict(self.state)
        base.update({
            "source": "world_space",
            "frame": int(self.frame_counter),
            "cycle_hint": round(self._cycle_phase(), 3),  # OK: phase is coordinate-like, not "time"
        })
        return base