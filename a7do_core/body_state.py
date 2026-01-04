# /a7do_core/body_state.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


@dataclass
class BodySignals:
    """
    Pure physiology (no symbols, no world-time awareness).
    Values are normalized to [0..1] for simplicity.
    """
    arousal: float = 0.10        # readiness/activation
    fatigue: float = 0.00        # grows while awake, recovers while asleep
    hunger: float = 0.20         # grows over time
    discomfort: float = 0.05     # wet/cold/pain/loudness etc.

    # Current stimulus level coming from experience layer (event intensity etc.)
    stimulus: float = 0.00


class BodyState:
    """
    Physiological substrate for A7DO.

    Key rule (Option A):
      - Wake/Sleep emerge from drives + stimulus.
      - Observer can *see* state but does not drive it.

    This class intentionally has:
      - no language
      - no concepts of time/day/night
      - no world access
    """

    def __init__(self):
        # Required by your UI snapshot (this is what was missing before)
        self.awake: bool = False

        # Signals
        self.sig = BodySignals()

        # Internal timers (minutes) used only for hysteresis (NOT "understood time")
        self._minutes_since_transition: float = 9999.0

        # Simple knobs (tune later)
        self._wake_hunger_threshold = 0.70
        self._wake_discomfort_threshold = 0.65
        self._wake_stimulus_threshold = 0.85

        self._sleep_fatigue_threshold = 0.80
        self._sleep_low_stimulus_threshold = 0.25

        # Prevent rapid flip-flop
        self._min_minutes_between_transitions = 20.0

    # ---------------------------------
    # External coupling (from events)
    # ---------------------------------
    def apply_intensity(self, intensity: float, *, discomfort_bias: float = 0.15) -> None:
        """
        Used by event_applier / experience blocks.
        Intensity drives arousal + (a little) discomfort.
        """
        i = _clamp(intensity)
        self.sig.stimulus = i

        # Stimulus increases arousal
        self.sig.arousal = _clamp(self.sig.arousal + 0.25 * i)

        # Some stimulus is uncomfortable (noise/light/pressure)
        self.sig.discomfort = _clamp(self.sig.discomfort + discomfort_bias * i)

    def clear_stimulus(self) -> None:
        self.sig.stimulus = 0.0

    # ---------------------------------
    # Transitions
    # ---------------------------------
    def wake(self) -> None:
        self.awake = True
        self._minutes_since_transition = 0.0
        # waking spikes arousal a bit
        self.sig.arousal = _clamp(self.sig.arousal + 0.30)

    def sleep(self) -> None:
        self.awake = False
        self._minutes_since_transition = 0.0
        # sleep drops arousal
        self.sig.arousal = _clamp(self.sig.arousal - 0.25)

    # ---------------------------------
    # Core physiology loop
    # ---------------------------------
    def tick(self, minutes: float = 15.0) -> Dict[str, Any]:
        """
        Advance physiology. This is NOT "time awareness".
        It's just state evolution per step.

        Returns an observer-visible dict of what happened (optional).
        """
        m = max(0.0, float(minutes))
        self._minutes_since_transition += m

        # Convert minutes -> fraction of an hour for gentle rates
        h = m / 60.0

        # --- drive dynamics ---
        # Hunger always rises; faster when awake
        self.sig.hunger = _clamp(self.sig.hunger + (0.05 * h) + (0.08 * h if self.awake else 0.00))

        # Fatigue rises when awake, recovers when asleep
        if self.awake:
            self.sig.fatigue = _clamp(self.sig.fatigue + 0.10 * h + 0.05 * self.sig.arousal * h)
        else:
            self.sig.fatigue = _clamp(self.sig.fatigue - 0.16 * h)

        # Discomfort decays slowly, faster during sleep (settling)
        if self.awake:
            self.sig.discomfort = _clamp(self.sig.discomfort - 0.04 * h)
        else:
            self.sig.discomfort = _clamp(self.sig.discomfort - 0.10 * h)

        # Arousal decays unless stimulus keeps it up
        self.sig.arousal = _clamp(self.sig.arousal - (0.06 * h) + (0.10 * self.sig.stimulus * h))

        # Stimulus naturally fades each tick (prevents “stuck on stimulus”)
        self.sig.stimulus = _clamp(self.sig.stimulus - 0.25 * h)

        # --- emergent transitions (Option A) ---
        changed = None

        can_transition = self._minutes_since_transition >= self._min_minutes_between_transitions

        if can_transition and not self.awake:
            if (
                self.sig.hunger >= self._wake_hunger_threshold
                or self.sig.discomfort >= self._wake_discomfort_threshold
                or self.sig.stimulus >= self._wake_stimulus_threshold
            ):
                self.wake()
                changed = "auto_wake"

        if can_transition and self.awake:
            if (
                self.sig.fatigue >= self._sleep_fatigue_threshold
                and self.sig.stimulus <= self._sleep_low_stimulus_threshold
            ):
                self.sleep()
                changed = "auto_sleep"

        return {
            "changed": changed or "none",
            "awake": self.awake,
        }

    # ---------------------------------
    # Observer snapshot
    # ---------------------------------
    def snapshot(self) -> Dict[str, Any]:
        return {
            "awake": self.awake,
            "arousal": round(self.sig.arousal, 3),
            "fatigue": round(self.sig.fatigue, 3),
            "hunger": round(self.sig.hunger, 3),
            "discomfort": round(self.sig.discomfort, 3),
            "stimulus": round(self.sig.stimulus, 3),
            "minutes_since_transition": round(self._minutes_since_transition, 1),
        }