# world_core/salience_investigator_bot.py

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SalienceInvestigatorBot:
    """
    Accounting layer.
    - Ingests snapshots from: world_space, observer, walker, scout, surveyor
    - Builds evidence for first grounded symbol: TV
    - Produces "drawing" from surveyor surface grid + field signature
    """

    name: str = "Investigator-1"
    frame_counter: int = 0
    ledger: List[Dict[str, Any]] = field(default_factory=list)

    # Evidence store for TV binding (no language used until confidence)
    tv_evidence: Dict[str, Any] = field(default_factory=lambda: {
        "seen_red": 0,
        "seen_green": 0,
        "sound_when_green": 0,
        "toggles": 0,
        "last_color": None,
        "drawing": None,
        "bound": False,
        "label": None,
    })

    last_surveyor_surface: Optional[List[List[int]]] = None

    def ingest(self, snap: Dict[str, Any]):
        if not isinstance(snap, dict):
            return

        src = snap.get("source", "unknown")
        frame = snap.get("frame", None)
        if isinstance(frame, int):
            self.frame_counter = max(self.frame_counter, frame)

        # Raw ledger record
        self.ledger.append({
            "tx_type": "ingest",
            "source": src,
            "frame": frame,
            "data": snap,
        })

        # Track latest surveyor drawing
        if src == "surveyor":
            surf = snap.get("surface_grid")
            if isinstance(surf, list) and surf:
                self.last_surveyor_surface = surf

        # Use observer/scout to build field evidence (red/green + sound coupling)
        if src in ("observer", "scout"):
            self._update_tv_evidence_from_fields(snap)

        # Attempt binding if enough evidence accumulated
        self._attempt_bind_tv()

    def _update_tv_evidence_from_fields(self, snap: Dict[str, Any]):
        ev = self.tv_evidence

        # Scout format
        if snap.get("source") == "scout":
            light = snap.get("light_now", {})
            color = light.get("color", None)
            sound = snap.get("sound_now", 0.0)
            self._accumulate_color_sound(ev, color, sound)
            return

        # Observer format: scan fields for object light + sound
        fields = snap.get("fields", [])
        if not isinstance(fields, list):
            return

        # Try to find "object tv" readings in any room
        obj_light = None
        obj_sound = None

        for f in fields:
            if not isinstance(f, dict):
                continue
            if f.get("scope") == "object" and f.get("object") == "tv":
                if f.get("type") == "light":
                    obj_light = f
                if f.get("type") == "sound":
                    obj_sound = f

        color = obj_light.get("color") if obj_light else None
        sound = float(obj_sound.get("level", 0.0)) if obj_sound else 0.0
        self._accumulate_color_sound(ev, color, sound)

    def _accumulate_color_sound(self, ev: Dict[str, Any], color: Any, sound: float):
        if color == "red":
            ev["seen_red"] += 1
        elif color == "green":
            ev["seen_green"] += 1
            if sound >= 0.05:
                ev["sound_when_green"] += 1

        # Toggle detection: change in color
        if color in ("red", "green") and ev["last_color"] in ("red", "green") and color != ev["last_color"]:
            ev["toggles"] += 1
        if color in ("red", "green"):
            ev["last_color"] = color

    def _attempt_bind_tv(self):
        ev = self.tv_evidence
        if ev["bound"]:
            return

        # Minimum evidence: observed both red and green + at least 2 toggles
        if ev["seen_red"] >= 3 and ev["seen_green"] >= 3 and ev["toggles"] >= 2:
            # Create a "drawing": store the most recent surface grid (downstream can learn it)
            ev["drawing"] = self.last_surveyor_surface
            ev["bound"] = True
            # Label now becomes allowed (symbol emerges)
            ev["label"] = "TV"

            self.ledger.append({
                "tx_type": "binding",
                "source": "salience_investigator",
                "frame": self.frame_counter,
                "data": {
                    "label": "TV",
                    "evidence": {
                        "seen_red": ev["seen_red"],
                        "seen_green": ev["seen_green"],
                        "toggles": ev["toggles"],
                        "sound_when_green": ev["sound_when_green"],
                    },
                    "drawing_attached": ev["drawing"] is not None,
                }
            })

    def snapshot(self) -> Dict[str, Any]:
        ev = self.tv_evidence
        return {
            "name": self.name,
            "source": "salience_investigator",
            "frame_counter": self.frame_counter,
            "total_transactions": len(self.ledger),
            "tv_binding": {
                "bound": ev["bound"],
                "label": ev["label"],
                "seen_red": ev["seen_red"],
                "seen_green": ev["seen_green"],
                "toggles": ev["toggles"],
                "sound_when_green": ev["sound_when_green"],
                "has_drawing": ev["drawing"] is not None,
            }
        }