# world_core/architect_bot.py

from typing import Dict, Any, List


class ArchitectBot:
    """
    Converts verified structures into blueprints.

    - No world access
    - No perception
    - No language
    - Pure abstraction
    """

    def __init__(self):
        self.blueprints: List[Dict[str, Any]] = []
        self.frame_counter = 0

    # -------------------------------------------------
    # Ingest confirmed structures
    # -------------------------------------------------

    def ingest(self, reception_snapshot: Dict[str, Any]):
        self.frame_counter += 1

        rooms = reception_snapshot.get("rooms", [])
        for room in rooms:
            blueprint = self._create_blueprint(room)
            if blueprint:
                self.blueprints.append(blueprint)

    # -------------------------------------------------
    # Blueprint generation
    # -------------------------------------------------

    def _create_blueprint(self, room: Dict[str, Any]) -> Dict[str, Any]:
        """
        Turn a room definition into a construction plan.
        """

        cluster = room.get("cluster_key")
        if not cluster:
            return {}

        blueprint = {
            "type": "blueprint",
            "structure": "room",
            "id": room["id"],
            "floor": room.get("floor", 0),
            "anchor_cluster": cluster,
            "components": [
                {"element": "wall", "count": 4},
                {"element": "floor", "count": 1},
                {"element": "ceiling", "count": 1},
            ],
            "constraints": {
                "enclosure": True,
                "planar": True,
            },
            "frame": self.frame_counter,
        }

        return blueprint

    # -------------------------------------------------
    # Snapshot
    # -------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "architect",
            "frames": self.frame_counter,
            "blueprints": self.blueprints[-5:],
        }