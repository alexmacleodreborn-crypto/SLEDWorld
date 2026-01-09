# world_core/walker_bot.py

import math
import random
from datetime import datetime


class WalkerBot:
    """
    Physical actor.
    Generates causation (movement, interaction, emissions).
    """

    def __init__(self, name: str, start_xyz, world):
        self.name = name
        self.world = world

        self.position = list(map(float, start_xyz))
        self.speed_m_per_min = 1.2

        self.current_area = "world"
        self.heard_sound_level = 0.0
        self.emitted_sound_level = 0.0

        self.target = None
        self.target_label = None

        self._last_time = None
        self.ledger = []

        self._pick_new_target()

    # -------------------------------------------------
    # WORLD TICK
    # -------------------------------------------------
    def tick(self, clock):
        now = clock.world_datetime
        if self._last_time is None:
            self._last_time = now
            return

        delta_min = (now - self._last_time).total_seconds() / 60
        self._last_time = now

        if delta_min <= 0:
            return

        self._move(delta_min)
        self._auto_interact()

    # -------------------------------------------------
    # MOVEMENT
    # -------------------------------------------------
    def _pick_new_target(self):
        places = list(self.world.places.values())
        if not places:
            return

        place = random.choice(places)
        self.target = list(place.position)
        self.target_label = place.name

    def _move(self, minutes):
        if not self.target:
            self._pick_new_target()
            return

        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        dist = math.sqrt(dx * dx + dy * dy)

        step = self.speed_m_per_min * minutes
        if dist <= step:
            self.position[0] = self.target[0]
            self.position[1] = self.target[1]
            self._pick_new_target()
            return

        scale = step / dist
        self.position[0] += dx * scale
        self.position[1] += dy * scale

    # -------------------------------------------------
    # INTERACTION (TV, REMOTE, ETC.)
    # -------------------------------------------------
    def _auto_interact(self):
        """
        Random physical interactions.
        """
        if random.random() < 0.05:
            self.emitted_sound_level = 1.0
            self._log_event("tv_toggle", {"sound": 1.0})
        else:
            self.emitted_sound_level = 0.0

    # -------------------------------------------------
    # EVENT EXPORT → INVESTIGATOR
    # -------------------------------------------------
    def export_event(self):
        return {
            "source": self.name,
            "type": "physical",
            "position": tuple(round(v, 2) for v in self.position),
            "sound_emitted": self.emitted_sound_level,
        }

    # -------------------------------------------------
    # SNAPSHOT (UI)
    # -------------------------------------------------
    def snapshot(self):
        return {
            "agent": self.name,
            "type": "walker",
            "position": [round(v, 2) for v in self.position],
            "destination": self.target_label,
            "sound_emitted": self.emitted_sound_level,
        }

    def _log_event(self, event, payload=None):
        self.ledger.append({
            "event": event,
            "payload": payload or {},
        })