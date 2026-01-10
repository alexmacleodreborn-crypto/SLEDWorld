from world_core.ledger import LedgerEvent

class InvestigatorBot:
    """
    Normalises raw snapshots into ledger events.
    No semantics. No names. Just numeric evidence.
    """

    def ingest_snapshot(self, frame: int, snap: dict):
        out = []
        if not isinstance(snap, dict):
            return out

        src = snap.get("source", "unknown")

        # Walker interactions
        if src == "walker":
            if snap.get("last_interaction"):
                out.append(LedgerEvent(
                    frame=frame,
                    source="walker",
                    kind="walker_interaction",
                    payload={
                        "interaction": snap.get("last_interaction"),
                        "points_xy": snap.get("points_xy", []),
                    }
                ))

        # Scout peaks
        if src == "scout" and snap.get("mode") == "sound":
            pts = snap.get("peak_points_xy", [])
            if pts:
                out.append(LedgerEvent(
                    frame=frame,
                    source="scout:sound",
                    kind="sound_peaks",
                    payload={"points_xy": pts}
                ))

        if src == "scout" and snap.get("mode") == "light":
            pts = snap.get("peak_points_xy", [])
            if pts:
                out.append(LedgerEvent(
                    frame=frame,
                    source="scout:light",
                    kind="light_peaks",
                    payload={"points_xy": pts}
                ))

        # Surveyor surface points
        if src == "surveyor":
            pts = snap.get("surface_points_xy", [])
            if pts:
                out.append(LedgerEvent(
                    frame=frame,
                    source="surveyor",
                    kind="surface_points",
                    payload={"points_xy": pts}
                ))

        # Language events (when present)
        if src == "language":
            out.append(LedgerEvent(
                frame=frame,
                source="language",
                kind="language_event",
                payload=snap
            ))

        return out