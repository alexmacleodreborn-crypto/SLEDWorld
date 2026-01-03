# a7do_core/familiarity.py

from collections import defaultdict

class Familiarity:
    """
    Pre-symbolic exposure memory.
    This is NOT knowledge, NOT language, NOT belief.
    It is simply: 'I have experienced this before'.
    """

    def __init__(self):
        # pattern -> strength
        self.patterns = defaultdict(float)

    def observe(self, pattern: str, weight: float = 1.0):
        """
        Register exposure to a sensory/world pattern.
        """
        self.patterns[pattern] += max(0.0, weight)

    def strength(self, pattern: str) -> float:
        """
        How familiar is this pattern?
        """
        return self.patterns.get(pattern, 0.0)

    def snapshot(self):
        """
        Observer-visible only.
        """
        return dict(self.patterns)