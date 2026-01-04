class WorldState:
    """
    Container for the entire world.
    """

    def __init__(self, clock):
        self.clock = clock
        self.places = {}
        self.agents = []
        self.events = []

    def add_place(self, place):
        self.places[place.name] = place

    def add_agent(self, agent, place_name):
        place = self.places[place_name]
        place.enter(agent)
        self.agents.append(agent)

    def tick(self):
        for agent in self.agents:
            agent.tick(self.clock)

    def snapshot(self):
        return {
            "time": self.clock.snapshot(),
            "places": {k: v.snapshot() for k, v in self.places.items()},
            "agents": [a.snapshot() for a in self.agents],
        }