class LightSource:
    """
    Simple binary light emitter.
    No cognition. No decay logic here.
    """

    def __init__(self, name, position, base_level=1.0):
        self.name = name
        self.position = position
        self.base_level = base_level
        self.active = False

    def set_active(self, state: bool):
        self.active = state

    def get_level(self):
        return self.base_level if self.active else 0.0