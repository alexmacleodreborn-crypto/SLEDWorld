# world_core/builder_bot.py

from typing import Dict, Any, List


class BuilderBot:
    """
    Converts blueprints into constructive procedures.

    - Learns sequences
    - Learns counts
    - Learns adjacency
    """

    def __init__(self):
        self.procedures: List[Dict[str, Any]] = []
        self.frame_counter = 0

    # -------------------------------------------------
    # Ingest blueprints
    # -------------------------------------------------

    def ingest(self, blueprint: Dict[str, Any]):
        self.frame_counter += 1

        if blueprint.get("type") != "blueprint":
            return

        procedure = self._derive_procedure(blueprint)
        self.procedures.append(procedure)

    # -------------------------------------------------
    # Procedure derivation
    # -------------------------------------------------

    def _derive_procedure(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        steps = []

        for component in blueprint["components"]:
            element = component["element"]
            count = component["count"]

            steps.append({
                "action": "repeat_place",
                "element": element,
                "count": count,
            })

        return {
            "type": "construction_procedure",
            "structure": blueprint["structure"],
            "id": blueprint["id"],
            "steps": steps,
            "constraints": blueprint["constraints"],
            "frame": self.frame_counter,
        }

    # -------------------------------------------------
    # Snapshot
    # -------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "source": "builder",
            "frames": self.frame_counter,
            "procedures": self.procedures[-5:],
        }