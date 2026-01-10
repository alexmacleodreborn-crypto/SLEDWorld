class ManagerBot:
    """
    Authority. Not intelligence.
    Holds manual approvals.
    """
    def __init__(self):
        self._approvals = {
            "neighbourhood": False,
            "population": False,
            "architect": False,
            "builder": False,
        }

    def manual_approve(self, key: str):
        if key in self._approvals:
            self._approvals[key] = True

    def approved(self, key: str) -> bool:
        return bool(self._approvals.get(key, False))

    def snapshot(self):
        return {
            "source": "manager",
            "approvals": dict(self._approvals)
        }