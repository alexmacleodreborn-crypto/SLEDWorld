class MemoryStore:
    """
    Placeholder memory substrate.

    At this stage, A7DO does not form episodic memories.
    This class exists so higher layers can attach later
    without refactoring the core.
    """

    def __init__(self):
        self.entries = []

    def store(self, item):
        self.entries.append(item)

    def all(self):
        return list(self.entries)