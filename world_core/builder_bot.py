# world_core/builder_bot.py

class BuilderBot:
    """
    Takes Architect structures and tries to assemble higher-level forms (wall->room).
    Stage-0: rule-based inference only.
    """

    def __init__(self, name="Builder-1"):
        self.name = name
        self.last_snapshot = {"source": "builder", "name": self.name, "inferences": []}

    def observe(self, world):
        # If Architect exists, read it
        architect = None
        for a in getattr(world, "agents", []):
            if a.__class__.__name__ == "ArchitectBot":
                architect = a
                break

        structs = architect.snapshot().get("structures", []) if architect else []

        inferences = []
        # Simple rule: if wall confidence high -> room candidate
        for s in structs:
            if s.get("label") == "candidate_wall" and s.get("confidence", 0) >= 0.6:
                inferences.append({"label": "candidate_room", "confidence": 0.5})

        self.last_snapshot = {
            "source": "builder",
            "name": self.name,
            "frame": getattr(world, "frame", None),
            "inferences": inferences
        }

    def snapshot(self):
        return self.last_snapshot