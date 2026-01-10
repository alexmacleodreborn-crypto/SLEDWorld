# world_core/reception_bot.py

from typing import Dict, Any, List


class ReceptionBot:
    """
    Structural verifier.

    Responsibilities:
    - Validate proposals using traction rules
    - Confirm rooms / floors / objects
    - Update world-structure ledger
    """

    def __init__(self):
        self.accepted: List[Dict[str, Any]] = []
        self.rejected: List[Dict[str, Any]] = []

        # Structural registry
        self.rooms = {}
        self.frame_counter = 0

    # -------------------------------------------------
    # Evaluate proposals
    # -------------------------------------------------

    def evaluate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        self.frame_counter += 1

        if proposal.get("type") != "structure_candidate":
            return {"status": "ignored"}

        evidence = proposal.get("evidence", [])
        if len(evidence) < 3:
            self.rejected.append(proposal)
            return {"status": "rejected", "reason": "insufficient_evidence"}

        # Traction check: persistence
        frames = {e.get("frame") for e in evidence if e.get("frame") is not None}
        if len(frames) < 2:
            self.rejected.append(proposal)
            return {"status": "rejected", "reason": "no_persistence"}

        # Traction check: survey surface present
        has_surface = any("surface_volume" in e for e in evidence)
        if not has_surface:
            self.rejected.append(proposal)
            return {"status": "rejected", "reason": "no_surface"}

        # ACCEPT — define a room
        room_id = f"room_{len(self.rooms)+1:03d}"

        room_record = {
            "id": room_id,
            "cluster_key": proposal["cluster_key"],
            "evidence_frames": sorted(frames),
            "floor": self._infer_floor(evidence),
            "status": "confirmed",
        }

        self.rooms[room_id] = room_record
        self.accepted.append(room_record)

        return {
            "status": "accepted",
            "room_id": room_id,
        }

    # -------------------------------------------------
    # Floor inference (simple, extendable)
    # -------------------------------------------------

    def _infer_floor(self, evidence: List[Dict[str, Any]]) -> int:
        zs = []
        for e in evidence:
            pos = e.get("position_xyz") or e.get("center_xyz")
            if pos:
                zs.append(pos[2])

        if not zs:
            return 0

        avg_z = sum(zs) / len(zs)
        return int(avg_z // 3)  # 3m floor height

    # -------------------------------------------------
    # Snapshot
    # -------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "reception",
            "frames": self.frame_counter,
            "rooms_confirmed": len(self.rooms),
            "rooms": list(self.rooms.values())[-5:],
        }