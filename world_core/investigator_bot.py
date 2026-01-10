# world_core/investigator_bot.py

from typing import Dict, Any, List
from world_core.ledger_event import LedgerEvent

class InvestigatorBot:
    """
    Process bot. Normalises streams into LedgerEvents.
    No approvals. No semantics.
    """
    def __init__(self, name="Investigator-1"):
        self.name = name
        self.frame_counter = 0
        self.buffer: List[LedgerEvent] = []

    def ingest_snapshot(self, frame: int, snap: Dict[str, Any]) -> List[LedgerEvent]:
        self.frame_counter = frame
        out: List[LedgerEvent] = []

        source = snap.get("source", "unknown")
        entity = snap.get("entity", snap.get("name", source))

        # Heuristics per source type
        if source in ("observer", "walker"):
            payload = {
                "position_xyz": snap.get("position_xyz"),
                "current_area": snap.get("current_area"),
                "heard_sound_level": snap.get("heard_sound_level"),
                "seen_light_level": snap.get("seen_light_level"),
                "seen_light_color": snap.get("seen_light_color"),
                "tv_state": snap.get("tv_state"),
            }
            out.append(LedgerEvent(frame=frame, source=source, entity=entity, kind="percept", payload=payload, confidence=0.6))

            # Add a point for square gate (map x,y into 32x32 roughly)
            pos = snap.get("position_xyz")
            if isinstance(pos, list) and len(pos) >= 2:
                y = int(abs(pos[1]) % 32)
                x = int(abs(pos[0]) % 32)
                out.append(LedgerEvent(frame=frame, source=source, entity=entity, kind="point", payload={"point_yx": (y, x)}, confidence=0.4))

        elif source in ("scout",):
            out.append(LedgerEvent(frame=frame, source=source, entity=entity, kind="field", payload={
                "mode": snap.get("mode"),
                "center_xyz": snap.get("center_xyz"),
                "resolution_m": snap.get("resolution_m"),
                "extent_m": snap.get("extent_m"),
                "summary": snap.get("summary"),
            }, confidence=0.55))

        elif source in ("surveyor",):
            out.append(LedgerEvent(frame=frame, source=source, entity=entity, kind="survey", payload={
                "center_xyz": snap.get("center_xyz"),
                "resolution_m": snap.get("resolution_m"),
                "volume_shape": snap.get("volume_shape"),
            }, confidence=0.65))

        elif source in ("symbol", "language"):
            out.append(LedgerEvent(frame=frame, source=source, entity=entity, kind="symbol", payload=snap, confidence=snap.get("confidence", 0.5)))

        return out

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "investigator",
            "name": self.name,
            "frame_counter": self.frame_counter,
        }