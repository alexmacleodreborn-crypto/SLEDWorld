# world_core/salience_investigator_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

@dataclass
class SalienceInvestigatorBot:
    """
    Single source of truth.
    Ingests snapshots; emits transactions + symbol promotions.
    Deploys scouts on salient changes (sound/light toggles).
    """
    frame_counter: int = 0
    ledger: List[Dict[str, Any]] = field(default_factory=list)

    # stable symbol store
    symbols: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # internal memory
    _last_tv_state: Optional[bool] = None
    _last_tv_light: Optional[str] = None
    _last_tv_sound: Optional[float] = None

    def ingest(self, snap: Dict[str, Any], world=None) -> None:
        if not isinstance(snap, dict) or "source" not in snap:
            return

        self.frame_counter = max(self.frame_counter, int(snap.get("frame", 0) or 0))

        src = snap.get("source")
        if src == "observer":
            self._handle_observer(snap, world)
        elif src == "surveyor":
            self._handle_surveyor(snap)
        elif src == "scout":
            self._handle_scout(snap)
        elif src == "walker":
            self._handle_walker(snap)

    def _tx(self, t: str, data: Dict[str, Any]):
        entry = {"frame": self.frame_counter, "type": t, **data}
        self.ledger.append(entry)

    def _handle_walker(self, snap, world):
        if snap.get("last_action"):
            self._tx("action", {"who": snap.get("name"), "action": snap.get("last_action"), "area": snap.get("current_area")})

    def _handle_observer(self, snap, world):
        # Detect TV via any seen object snapshot containing tv fields
        seen = snap.get("seen_objects", {})
        # pick first item that has 'is_on' or light_color fields
        tv_key = None
        tv = None
        for k, v in seen.items():
            if isinstance(v, dict) and ("is_on" in v or "light_color" in v or "sound_level" in v):
                tv_key = k
                tv = v
                break

        if tv is not None:
            is_on = tv.get("is_on")
            light_color = tv.get("light_color")
            sound_level = tv.get("sound_level")

            changed = False
            if self._last_tv_state is None:
                self._last_tv_state = is_on
                self._last_tv_light = light_color
                self._last_tv_sound = sound_level
            else:
                if is_on != self._last_tv_state:
                    self._tx("tv_state_change", {"key": tv_key, "from": self._last_tv_state, "to": is_on})
                    changed = True
                if light_color != self._last_tv_light:
                    self._tx("tv_light_change", {"key": tv_key, "from": self._last_tv_light, "to": light_color})
                    changed = True
                if sound_level != self._last_tv_sound:
                    self._tx("tv_sound_change", {"key": tv_key, "from": self._last_tv_sound, "to": sound_level})
                    changed = True

                self._last_tv_state = is_on
                self._last_tv_light = light_color
                self._last_tv_sound = sound_level

            # If changed, deploy scouts to confirm signatures
            if changed and world is not None:
                # use walker position if available, else tv position unknown -> use neighbourhood center
                walker = world.get_agent("WalkerBot")
                center = tuple(walker.position) if walker else world.surveyor.center_xyz
                world.deploy_scout("sound", center_xyz=center, name=f"Scout-sound-{self.frame_counter}", max_frames=25)
                world.deploy_scout("light", center_xyz=center, name=f"Scout-light-{self.frame_counter}", max_frames=25)

            # Promote symbol TV once we see correlated light+sound at least once
            self.symbols.setdefault("TV", {"symbol": "TV", "confidence": 0.5})
            self.symbols["TV"]["confidence"] = min(1.0, self.symbols["TV"]["confidence"] + 0.05)

            if light_color in ("red", "green"):
                self.symbols.setdefault("COLOR", {"symbol": "COLOR", "confidence": 0.4})
                self.symbols["COLOR"]["confidence"] = min(1.0, self.symbols["COLOR"]["confidence"] + 0.02)
                # store grounded color tokens
                self.symbols.setdefault(f"COLOR_{light_color.upper()}", {"symbol": f"COLOR_{light_color.upper()}", "confidence": 0.6})

            if is_on is not None:
                self.symbols.setdefault("ONOFF", {"symbol": "ONOFF", "confidence": 0.5})
                self.symbols["ONOFF"]["confidence"] = min(1.0, self.symbols["ONOFF"]["confidence"] + 0.02)
                self.symbols.setdefault("ON", {"symbol": "ON", "confidence": 0.6})
                self.symbols.setdefault("OFF", {"symbol": "OFF", "confidence": 0.6})

    def _handle_surveyor(self, snap):
        # aerial grid exists: allows structural promotions later
        if "aerial_grid" in snap:
            self._tx("aerial_update", {"note": "aerial_grid_updated"})
            self.symbols.setdefault("AERIAL_MAP", {"symbol": "AERIAL_MAP", "confidence": 0.7})
            self.symbols["AERIAL_MAP"]["confidence"] = min(1.0, self.symbols["AERIAL_MAP"]["confidence"] + 0.01)

    def _handle_scout(self, snap):
        # simply log receipt; later used for signatures
        self._tx("scout_report", {"name": snap.get("name"), "signal": snap.get("signal")})

        sig = snap.get("signal")
        if sig == "sound":
            self.symbols.setdefault("SOUND_FIELD", {"symbol": "SOUND_FIELD", "confidence": 0.5})
            self.symbols["SOUND_FIELD"]["confidence"] = min(1.0, self.symbols["SOUND_FIELD"]["confidence"] + 0.02)
        if sig == "light":
            self.symbols.setdefault("LIGHT_FIELD", {"symbol": "LIGHT_FIELD", "confidence": 0.5})
            self.symbols["LIGHT_FIELD"]["confidence"] = min(1.0, self.symbols["LIGHT_FIELD"]["confidence"] + 0.02)
        if sig == "shape":
            self.symbols.setdefault("SHAPE_FIELD", {"symbol": "SHAPE_FIELD", "confidence": 0.5})
            self.symbols["SHAPE_FIELD"]["confidence"] = min(1.0, self.symbols["SHAPE_FIELD"]["confidence"] + 0.02)

    def apply_structures(self, validations: List[Dict[str, Any]]):
        # Builder confirmations promote stable structural symbols
        for v in validations:
            if v.get("status") == "confirmed":
                sym = v.get("structure")
                if not sym:
                    continue
                self.symbols.setdefault(sym, {"symbol": sym, "confidence": 0.7})
                self.symbols[sym]["confidence"] = min(1.0, self.symbols[sym]["confidence"] + 0.05)
                self._tx("structure_confirmed", {"structure": sym, "match": v.get("match")})

    def snapshot(self):
        return {
            "frame_counter": self.frame_counter,
            "ledger_len": len(self.ledger),
            "symbols": self.symbols,
        }