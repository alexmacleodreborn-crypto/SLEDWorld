# world_core/salience_investigator_bot.py

from __future__ import annotations
from typing import Dict, Any, List


class SalienceInvestigatorBot:
    """
    Ledger / single source of truth.

    - Consumes snapshots from all world-creator bots
    - Tracks persistence and correlations
    - Promotes patterns → symbols
    - NEVER crashes on unknown input
    """

    def __init__(self):
        self.frame_counter = 0
        self.ledger: List[Dict[str, Any]] = []

        # Simple persistence trackers
        self._seen_objects = {}
        self._last_states = {}

    # =================================================
    # PUBLIC INGEST API (SAFE)
    # =================================================

    def ingest(self, snap: Dict[str, Any], world=None):
        """
        Main entry point.
        Defensive: never assume structure.
        """
        if not isinstance(snap, dict):
            return

        source = snap.get("source", "unknown")

        self.frame_counter += 1

        handler = {
            "walker": self._handle_walker,
            "observer": self._handle_observer,
            "scout": self._handle_scout,
            "surveyor": self._handle_surveyor,
            "world_space": self._handle_world_space,
        }.get(source, self._handle_unknown)

        try:
            handler(snap)
        except Exception as e:
            # Ledger must NEVER crash the world
            self.ledger.append({
                "frame": self.frame_counter,
                "type": "ledger_error",
                "source": source,
                "error": str(e),
            })

    # =================================================
    # HANDLERS (ROBUST, MINIMAL)
    # =================================================

    def _handle_walker(self, snap: Dict[str, Any]):
        """
        Walker = causation only.
        """
        entry = {
            "frame": self.frame_counter,
            "type": "walker_event",
            "position": snap.get("position_xyz"),
            "action": snap.get("action"),
            "area": snap.get("current_area"),
        }
        self.ledger.append(entry)

    def _handle_observer(self, snap: Dict[str, Any]):
        """
        Observer = perception.
        """
        seen = snap.get("seen_objects", {})
        for name, data in seen.items():
            prev = self._last_states.get(name)
            if prev != data:
                self.ledger.append({
                    "frame": self.frame_counter,
                    "type": "state_change",
                    "object": name,
                    "data": data,
                })
                self._last_states[name] = data

    def _handle_scout(self, snap: Dict[str, Any]):
        """
        Scout = focused sensing.
        """
        self.ledger.append({
            "frame": self.frame_counter,
            "type": "scout_report",
            "signal": snap.get("signal"),
            "persistence": snap.get("persistence"),
        })

    def _handle_surveyor(self, snap: Dict[str, Any]):
        """
        Surveyor = structure.
        """
        if "aerial_grid" in snap:
            self.ledger.append({
                "frame": self.frame_counter,
                "type": "aerial_update",
                "size": (
                    len(snap["aerial_grid"]),
                    len(snap["aerial_grid"][0]) if snap["aerial_grid"] else 0,
                ),
            })

    def _handle_world_space(self, snap: Dict[str, Any]):
        """
        Global environment.
        """
        self.ledger.append({
            "frame": self.frame_counter,
            "type": "environment",
            "light": snap.get("light_level"),
            "weather": snap.get("weather"),
        })

    def _handle_unknown(self, snap: Dict[str, Any]):
        """
        Future-proofing.
        """
        self.ledger.append({
            "frame": self.frame_counter,
            "type": "unknown_snapshot",
            "keys": list(snap.keys()),
        })

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self):
        return {
            "frames": self.frame_counter,
            "total_events": len(self.ledger),
            "recent": self.ledger[-10:],
        }