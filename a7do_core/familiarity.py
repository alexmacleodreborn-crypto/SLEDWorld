from collections import defaultdict

class FamiliarityStore:
    def __init__(self):
        self.scores = defaultdict(float)

    def reinforce(self, pattern, amount=1.0):
        self.scores[pattern] += amount

    def top(self, n):
        return sorted(self.scores.items(), key=lambda x: -x[1])[:n]