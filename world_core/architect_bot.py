class ArchitectBot:
    """
    Dormant until gates+approval.
    Produces simple structure plans from registry.
    """
    def __init__(self):
        self._plans = []

    def generate(self, registry):
        # Minimal demo: if rooms exist, propose a "structure plan"
        if registry.get("rooms"):
            self._plans.append({
                "type": "structure_plan",
                "summary": f"{len(registry['rooms'])} rooms observed",
            })
        self._plans = self._plans[-20:]

    def plans_tail(self, n=10):
        return self._plans[-int(n):]