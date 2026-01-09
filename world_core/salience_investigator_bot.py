# world_core/salience_investigator_bot.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple
import math
from collections import defaultdict, Counter


@dataclass
class SalienceInvestigatorBot:
    """
    Ledger = reality authority.
    Ingests snapshots from observer/walker/scout/surveyor and promotes:

      Surface pattern -> BRICK
      BRICK + strong planes -> WALL
      4 bounding WALLs -> ROOM
      Light+Sound state machine -> TV (stateful)

    Uses Architect + Builder + Language bots if attached.
    """

    name: str = "Ledger-1"
    frame_counter: int = 0
    ledger: List[Dict[str, Any]] = field(default_factory=list)
    transitions: List[Dict[str, Any]] = field(default_factory=list)

    # Symbol store
    symbols: Dict[str, Any] = field(default_factory=lambda: {"types": {}, "instances": []})

    # For transition detection
    _last_by_key: Dict[Tuple[str, str], Dict[str, Any]] = field(default_factory=dict)

    # Cached geometry summaries from surveyor
    geom: Dict[str, Any] = field(default_factory=dict)

    # External modules (optional)
    architect: Any = None
    builder: Any = None
    language: Any = None

    def attach(self, architect=None, builder=None, language=None):
        self.architect = architect
        self.builder = builder
        self.language = language

    # --------------------------
    # Ingest
    # --------------------------
    def ingest(self, snap: Dict[str, Any]):
        if not isinstance(snap, dict):
            return
        if "source" not in snap:
            return

        frame = int(snap.get("frame", 0) or 0)
        self.frame_counter = max(self.frame_counter, frame)

        entry = {
            "frame": frame,
            "source": snap.get("source"),
            "type": snap.get("type"),
            "name": snap.get("name"),
            "area": snap.get("current_area") or snap.get("area"),
            "bounds": snap.get("bounds") or snap.get("current_bounds"),
            "signals": snap.get("signals", {}) or {},
            # keep small: do not store huge volumes here
        }
        self.ledger.append(entry)

        # Transition detection (sound/light changes)
        key = (str(entry["source"]), str(entry.get("area") or entry.get("name") or "unknown"))
        prev = self._last_by_key.get(key)
        self._last_by_key[key] = entry

        if prev:
            self._detect_transitions(prev, entry)

    def _detect_transitions(self, prev: Dict[str, Any], cur: Dict[str, Any]):
        psig = prev.get("signals", {}) or {}
        csig = cur.get("signals", {}) or {}

        # sound
        if "sound" in psig or "sound" in csig:
            ps = float(psig.get("sound", 0.0) or 0.0)
            cs = float(csig.get("sound", 0.0) or 0.0)
            if abs(cs - ps) >= 0.2:
                self.transitions.append({
                    "frame": cur["frame"],
                    "event": "sound_change",
                    "key": [prev["source"], prev.get("area") or prev.get("name") or "unknown"],
                    "from": round(ps, 3),
                    "to": round(cs, 3),
                })

        # light
        pl = psig.get("light", None)
        cl = csig.get("light", None)
        if isinstance(pl, dict) and isinstance(cl, dict):
            pi = float(pl.get("intensity", 0.0) or 0.0)
            ci = float(cl.get("intensity", 0.0) or 0.0)
            pc = str(pl.get("color", "none"))
            cc = str(cl.get("color", "none"))

            if abs(ci - pi) >= 0.2 or cc != pc:
                self.transitions.append({
                    "frame": cur["frame"],
                    "event": "light_change",
                    "key": [prev["source"], prev.get("area") or prev.get("name") or "unknown"],
                    "from": {"intensity": round(pi, 3), "color": pc},
                    "to": {"intensity": round(ci, 3), "color": cc},
                })

        if len(self.transitions) > 500:
            self.transitions = self.transitions[-500:]

    # --------------------------
    # Geometry summarisation from Surveyor
    # --------------------------
    def ingest_surveyor_snapshot(self, surveyor_snap: Dict[str, Any]):
        """
        surveyor_snap may contain surface_volume (smallish).
        We summarise into dominant planes so higher layers stay cheap.
        """
        if not isinstance(surveyor_snap, dict):
            return
        if surveyor_snap.get("source") != "surveyor":
            return

        frame = int(surveyor_snap.get("frame", self.frame_counter) or self.frame_counter)
        self.frame_counter = max(self.frame_counter, frame)

        surf = surveyor_snap.get("surface_volume", None)
        if surf is None:
            return

        # surf: [z][y][x] binary
        nz = len(surf)
        ny = len(surf[0]) if nz else 0
        nx = len(surf[0][0]) if (nz and ny) else 0

        # Count surface voxels per x-plane and y-plane (across all z)
        x_counts = [0] * nx
        y_counts = [0] * ny
        total = 0

        for iz in range(nz):
            for iy in range(ny):
                row = surf[iz][iy]
                for ix in range(nx):
                    if row[ix] == 1:
                        total += 1
                        x_counts[ix] += 1
                        y_counts[iy] += 1

        def top_planes(counts, axis: str, k=4):
            if not counts:
                return []
            m = max(counts) if counts else 0
            if m <= 0:
                return []
            # threshold to avoid noise
            thresh = 0.35 * m
            planes = []
            for i, c in enumerate(counts):
                if c >= thresh:
                    planes.append({"idx": i, "support": c / (m + 1e-9)})
            # Take top k by support
            planes = sorted(planes, key=lambda d: d["support"], reverse=True)[:k]
            return planes

        planes_x = top_planes(x_counts, "x")
        planes_y = top_planes(y_counts, "y")

        # Convert idx -> world coord approximation
        cx, cy, cz = surveyor_snap.get("center_xyz", (0.0, 0.0, 0.0))
        r = float(surveyor_snap.get("extent_m", 10.0) or 10.0)
        step = float(surveyor_snap.get("resolution_m", 1.0) or 1.0)

        def idx_to_coord(axis: str, idx: int):
            if axis == "x":
                return (cx - r) + idx * step
            if axis == "y":
                return (cy - r) + idx * step
            return 0.0

        self.geom = {
            "frame": frame,
            "volume_shape": surveyor_snap.get("volume_shape", (nz, ny, nx)),
            "total_surface_voxels": total,
            "planes": {
                "x": [{"coord": idx_to_coord("x", p["idx"]), "support": p["support"], "idx": p["idx"]} for p in planes_x],
                "y": [{"coord": idx_to_coord("y", p["idx"]), "support": p["support"], "idx": p["idx"]} for p in planes_y],
            },
        }

    # --------------------------
    # Promotion rules
    # --------------------------
    def promote(self):
        """
        Run promotions once per frame (after all ingests).
        """
        frame = self.frame_counter

        # --- TV symbol: detect stable state machine from light/sound transitions
        tv_conf = self._tv_confidence()
        if tv_conf >= 0.8:
            self._ensure_symbol_type("TV", confidence=tv_conf, meta={"stateful": True, "signals": ["sound", "light"]})

        # --- BRICK symbol: if we have strong surface planes and persistence
        brick_conf = self._brick_confidence()
        if brick_conf >= 0.75:
            # Derived "brick size" from survey resolution as a placeholder emergent scale.
            # This is not hard-coded as an object; it's a compression unit.
            step = 1.0
            if self.geom:
                # infer step from plane coord spacing if possible; else keep 1.0
                step = 1.0
            self._ensure_symbol_type("BRICK", confidence=brick_conf, meta={"unit": "surface_repeat", "scale_hint_m": step})

        # --- Architect + Builder pathway for WALL / ROOM
        if self.architect and self.builder and self.geom and "BRICK" in self.symbols["types"]:
            proposals = self.architect.propose(frame=frame, symbols=self.symbols, geom=self.geom)
            validations = self.builder.validate(frame=frame, proposals=proposals, geom=self.geom)

            # Promote WALL if any validation score high
            wall_scores = [v["score"] for v in validations if v["type"] == "WALL_VALIDATION"]
            if wall_scores and max(wall_scores) >= 0.75:
                self._ensure_symbol_type("WALL", confidence=max(wall_scores), meta={"from": "BRICK+planes"})

            # Promote ROOM if room validation high and we have WALL
            room_scores = [v["score"] for v in validations if v["type"] == "ROOM_VALIDATION"]
            if room_scores and max(room_scores) >= 0.75 and "WALL" in self.symbols["types"]:
                self._ensure_symbol_type("ROOM", confidence=max(room_scores), meta={"from": "4 walls enclosure"})

        # --- Language update (late-stage)
        if self.language:
            self.language.update(frame=frame, symbols=self.symbols, transitions=self.transitions)

    def _ensure_symbol_type(self, sym: str, confidence: float, meta: Dict[str, Any] | None = None):
        cur = self.symbols["types"].get(sym)
        if cur is None:
            self.symbols["types"][sym] = {
                "confidence": round(float(confidence), 3),
                "first_frame": self.frame_counter,
                "meta": meta or {},
            }
        else:
            # confidence can only increase slowly (persistence)
            cur_conf = float(cur.get("confidence", 0.0) or 0.0)
            new_conf = max(cur_conf, float(confidence))
            cur["confidence"] = round(min(new_conf, 0.999), 3)
            if meta:
                cur_meta = cur.get("meta", {}) or {}
                cur_meta.update(meta)
                cur["meta"] = cur_meta

    def _tv_confidence(self) -> float:
        """
        TV emerges when both sound and light transitions happen repeatedly.
        """
        lc = sum(1 for t in self.transitions[-120:] if t.get("event") == "light_change")
        sc = sum(1 for t in self.transitions[-120:] if t.get("event") == "sound_change")
        # Need at least a couple of toggles
        if lc >= 2 and sc >= 2:
            return 0.8 + min(0.15, 0.02 * (lc + sc))
        if lc >= 1 and sc >= 1:
            return 0.7
        return 0.0

    def _brick_confidence(self) -> float:
        """
        BRICK emerges when we have stable strong planes and enough surface data.
        """
        if not self.geom:
            return 0.0
        total = self.geom.get("total_surface_voxels", 0) or 0
        px = self.geom.get("planes", {}).get("x", [])
        py = self.geom.get("planes", {}).get("y", [])

        strong = sum(1 for p in (px + py) if p.get("support", 0.0) >= 0.7)
        if total > 50 and strong >= 2:
            return 0.75 + min(0.2, 0.05 * (strong - 1))
        if total > 30 and strong >= 1:
            return 0.65
        return 0.0

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "ledger",
            "name": self.name,
            "frame": self.frame_counter,
            "total_entries": len(self.ledger),
            "total_transitions": len(self.transitions),
            "symbols": self.symbols,
            "geom": self.geom,
            "transitions_tail": self.transitions[-15:],
            "ledger_tail": self.ledger[-15:],
        }