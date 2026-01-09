# inside WorldState.tick()

# 1. advance agents
for agent in self.agents:
    if hasattr(agent, "tick"):
        agent.tick(self.clock)
    if hasattr(agent, "observe"):
        agent.observe(self)

# 2. ingest snapshots
for agent in self.agents:
    if hasattr(agent, "snapshot"):
        snap = agent.snapshot()
        if isinstance(snap, dict):
            self.ledger.ingest(snap, world=self)

# 3. ingest world space
space_snap = self.space.snapshot()
self.ledger.ingest(space_snap, world=self)