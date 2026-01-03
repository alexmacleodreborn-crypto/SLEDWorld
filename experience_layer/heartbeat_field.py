import math
import random
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


# -----------------------------
#  World clock (authoritative)
# -----------------------------
@dataclass
class WorldClock:
    total_seconds: float = 0.0

    def tick(self, dt_seconds: float) -> None:
        # dt_seconds should be derived from your chosen "minutes per refresh"
        self.total_seconds += float(dt_seconds)

    @property
    def days_elapsed(self) -> float:
        return self.total_seconds / 86400.0

    def snapshot(self) -> Dict[str, float]:
        minutes = self.total_seconds / 60.0
        hours = minutes / 60.0
        return {
            "total_seconds": self.total_seconds,
            "total_minutes": minutes,
            "total_hours": hours,
            "total_days": self.days_elapsed,
        }


# -----------------------------
#  Heartbeat signals (continuous)
# -----------------------------
@dataclass
class HeartbeatSignal:
    bpm: float
    amplitude: float
    phase: float = field(default_factory=lambda: random.random() * 2.0 * math.pi)

    def hz(self) -> float:
        return self.bpm / 60.0

    def wave(self, t_seconds: float) -> float:
        # Continuous oscillation
        f = self.hz()
        return self.amplitude * math.sin(2.0 * math.pi * f * t_seconds + self.phase)

    def envelope(self, t_seconds: float, wander_strength: float = 0.03) -> float:
        """
        Optional slow amplitude modulation ("physiological wander").
        Keep small to avoid fake chaos.
        """
        # Very low frequency mod to avoid "perfect metronome"
        slow = math.sin(2.0 * math.pi * (1.0 / 30.0) * (t_seconds / 60.0) + self.phase * 0.3)
        return 1.0 + wander_strength * slow

    def wave_wander(self, t_seconds: float) -> float:
        return self.wave(t_seconds) * self.envelope(t_seconds)


# -----------------------------
#  Gestation gain (muted → strong)
# -----------------------------
def gestation_gain(gestation_days: float, term_days: float = 270.0) -> float:
    # Linear ramp is fine to start (simple + stable)
    g = max(0.0, min(1.0, float(gestation_days) / float(term_days)))
    return g


# -----------------------------
#  Birth shock (smooth discontinuity)
# -----------------------------
def smooth_step(x: float) -> float:
    # 0..1 cubic smoothstep
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


@dataclass
class BirthShock:
    """
    Models the transition from womb → external world.
    Not a single spike; a short window of rising intensity.
    """
    birth_time_s: float                      # world seconds when birth begins
    duration_s: float = 120.0                # 2 minutes transition window (tunable)

    def progress(self, t_s: float) -> float:
        # 0 pre-birth; 1 after duration
        return smooth_step((t_s - self.birth_time_s) / self.duration_s)

    def channels(self, t_s: float) -> Dict[str, float]:
        """
        Returns additive shock channels that increase during transition.
        Keep values in 0..1-ish ranges.
        """
        p = self.progress(t_s)
        # Post-birth: light + air pressure + noise + breathing rhythm onset
        # These are "math knobs" - later you can make them place/weather-dependent.
        return {
            "light": 0.9 * p,
            "air": 0.7 * p,
            "noise": 0.8 * p,
            "cold": 0.5 * p,
            "breath": 0.6 * p,
        }


# -----------------------------
#  Coupling: mother + a7do -> perceived sensory field
# -----------------------------
@dataclass
class CoupledFieldModel:
    mother: HeartbeatSignal
    a7do: HeartbeatSignal
    w_mother: float = 0.85
    w_a7do: float = 0.15

    def composite_pressure(self, t_s: float) -> float:
        hm = self.mother.wave_wander(t_s)
        ha = self.a7do.wave_wander(t_s)
        return self.w_mother * hm + self.w_a7do * ha

    def sensory_snapshot_prebirth(self, t_s: float, gestation_days: float) -> Dict[str, float]:
        """
        Prebirth: muted imprinting, filtered channels.
        """
        g = gestation_gain(gestation_days)
        p = self.composite_pressure(t_s)

        # Prebirth sensory channels: pressure/vibration dominate; light is low
        # Use abs() so intensity is non-negative and feels like "pulses"
        return {
            "pressure": abs(p) * (0.6 + 0.4 * g),
            "vibration": abs(self.mother.wave_wander(t_s)) * (0.7 + 0.3 * g),
            "internal_rhythm": abs(self.a7do.wave_wander(t_s)) * (0.4 + 0.6 * g),
            "light": 0.05 * g,
            "noise": 0.10 * g,
        }

    def sensory_snapshot_postbirth(
        self,
        t_s: float,
        gestation_days: float,
        shock: BirthShock,
        mother_attenuation: float = 0.25,
        a7do_amplify: float = 1.8,
    ) -> Dict[str, float]:
        """
        Postbirth: mother becomes less dominant; external channels appear.
        """
        # We keep gestation_gain as a general "development gain" knob too.
        g = gestation_gain(gestation_days)

        # Attenuate mother conduction; amplify internal heartbeat salience
        hm = self.mother.wave_wander(t_s) * mother_attenuation
        ha = self.a7do.wave_wander(t_s) * a7do_amplify
        p = self.w_mother * hm + self.w_a7do * ha

        base = {
            "pressure": abs(p) * (0.7 + 0.3 * g),
            "vibration": abs(hm) * (0.4 + 0.2 * g),
            "internal_rhythm": abs(ha) * (0.6 + 0.4 * g),
        }

        # Add shock channels
        sh = shock.channels(t_s)
        # Blend: base + shock (cap at 1.0-ish if you want)
        out = {**base}
        for k, v in sh.items():
            out[k] = out.get(k, 0.0) + float(v)

        return out


# -----------------------------
#  Simple: birth time selection
# -----------------------------
def birth_time_from_days(birth_day: float) -> float:
    return float(birth_day) * 86400.0