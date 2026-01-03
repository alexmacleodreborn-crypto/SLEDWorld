class InternalLog:
    def __init__(self):
        self.entries = []

    def add(self, text: str):
        self.entries.append(str(text))