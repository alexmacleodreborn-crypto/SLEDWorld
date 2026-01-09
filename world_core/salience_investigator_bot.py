# world_core/salience_investigator_bot.py

class SalienceInvestigatorBot:
    """
    Accounting / transaction ledger.

    Accepts any snapshot with:
      - source
      - frame
      - signals

    Records:
      - raw ledger entries
      - detected transitions (light/sound changes)
    """

    def __init__(self):
        self.frame_counter = 0
        self.ledger = []
        self.transitions = []
        self._last_by_key = {}

    def ingest(self, snap: dict):
        if not isinstance(snap, dict):
            return
        if "source" not in snap:
            return

        self.frame_counter = max(self.frame_counter, int(snap.get("frame", 0) or 0))

        entry = {
            "frame": int(snap.get("frame", 0) or 0),
            "source": snap.get("source"),
            "type": snap.get("type"),
            "name": snap.get("name"),
            "area": snap.get("current_area") or snap.get("area"),
            "signals": snap.get("signals", {}) or {},
        }
        self.ledger.append(entry)

        # Detect simple transitions on (source, area/name)
        key = (entry["source"], entry.get("area") or entry.get("name") or "unknown")

        prev = self._last_by_key.get(key)
        self._last_by_key[key] = entry

        if not prev:
            return

        prev_sig = prev.get("signals", {}) or {}
        cur_sig = entry.get("signals", {}) or {}

        # Sound transition
        ps = float(prev_sig.get("sound", 0.0) or 0.0) if "sound" in prev_sig else None
        cs = float(cur_sig.get("sound", 0.0) or 0.0) if "sound" in cur_sig else None

        if ps is not None and cs is not None and abs(cs - ps) >= 0.2:
            self.transitions.append({
                "frame": entry["frame"],
                "event": "sound_change",
                "key": list(key),
                "from": round(ps, 3),
                "to": round(cs, 3),
            })

        # Light transition
        pl = prev_sig.get("light", None)
        cl = cur_sig.get("light", None)

        if isinstance(pl, dict) and isinstance(cl, dict):
            pi = float(pl.get("intensity", 0.0) or 0.0)
            ci = float(cl.get("intensity", 0.0) or 0.0)
            pc = str(pl.get("color", "none"))
            cc = str(cl.get("color", "none"))

            if abs(ci - pi) >= 0.2 or cc != pc:
                self.transitions.append({
                    "frame": entry["frame"],
                    "event": "light_change",
                    "key": list(key),
                    "from": {"intensity": round(pi, 3), "color": pc},
                    "to": {"intensity": round(ci, 3), "color": cc},
                })

    def snapshot(self):
        return {
            "frames_processed": self.frame_counter,
            "total_entries": len(self.ledger),
            "total_transitions": len(self.transitions),
            "transitions_tail": self.transitions[-10:],
        }