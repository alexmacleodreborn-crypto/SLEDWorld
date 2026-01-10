# world_core/builder_bot.py
from typing import Dict, Any, List

class BuilderBot:
    def __init__(self, name="Builder-1"):
        self.name = name
        self.actions: List[Dict[str, Any]] = []

    def execute(self, manager_decision: Dict[str, Any], architect_plans_tail: List[Dict[str, Any]]):
        if not manager_decision.get("approve_structure"):
            return
        if architect_plans_tail:
            self.actions.append({"frame": manager_decision.get("frame"), "action":"queue_build", "plan": architect_plans_tail[-1]})

    def snapshot(self):
        return {"source":"builder","name":self.name,"actions_tail": self.actions[-20:]}