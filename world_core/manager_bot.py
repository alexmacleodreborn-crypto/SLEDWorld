# world_core/manager_bot.py
from typing import Dict, Any, List

class ManagerBot:
    def __init__(self, name="Manager-1"):
        self.name = name
        self.decisions: List[Dict[str, Any]] = []

    def decide(self, ledger_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        gates = ledger_snapshot.get("manager_approval", {})
        decision = {
            "frame": ledger_snapshot.get("frame", 0),
            "approve_patterns": bool(gates.get("patterns_stable", False)),
            "approve_structure": bool(gates.get("structure_confirmed", False)),
            "approve_language": bool(gates.get("language_ready", False)),
        }
        self.decisions.append(decision)
        return decision

    def snapshot(self):
        return {"source":"manager","name":self.name,"decisions_tail": self.decisions[-20:]}