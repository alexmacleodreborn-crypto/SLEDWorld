class Place:
    """
    Physical location in the world.
    """

    def __init__(self, name):
        self.name = name
        self.agents = []

    def enter(self, agent):
        if agent not in self.agents:
            self.agents.append(agent)
            agent.location = self

    def leave(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)

    def snapshot(self):
        return {
            "name": self.name,
            "agents": [a.name for a in self.agents],
        }