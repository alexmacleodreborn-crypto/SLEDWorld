# world_core/architect_bot.py
from typing import Dict, Any, List

class ArchitectBot:
    def __init__(self, name="Architect-1"):
        self.name = name
        self.plans: List[Dict[str, Any]] = []

    def generate(self, reception_registry: Dict[str, Any]):
        # Minimal v1: emit a plan stub once places exist
        if reception_registry.get("places") and not self.plans:
            self.plans.append({"type":"world_schema","confidence":0.5,"places": list(reception_registry["places"].keys())})

    def plans_tail(self, n=10):
        return self.plans[-n:]

    def snapshot(self):
        return {"source":"architect","name":self.name,"plans_tail": self.plans[-10:]}