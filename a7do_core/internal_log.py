class InternalLog:
    def __init__(self):
        self.entries = []

    def add(self, text):
        self.entries.append(text)

    def tail(self, n):
        return self.entries[-n:]