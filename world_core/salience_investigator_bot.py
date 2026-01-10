class SalienceLedger:
    """
    Ledger is the final authority.
    All bots write here. Manager reads here and approves.
    """

    def __init__(self):
        self.events = []
        self.counter = 0

    def ingest(self, snap: dict, world=None):
        if not isinstance(snap, dict):
            return

        self.counter += 1
        event = dict(snap)

        # normalize metadata
        if "frame" not in event and world is not None and hasattr(world, "space"):
            event["frame"] = world.space.frame_counter

        if "source" not in event:
            event["source"] = event.get("type", "unknown")

        event["_id"] = self.counter
        self.events.append(event)

    def last(self, n=20):
        return self.events[-n:]