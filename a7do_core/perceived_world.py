class PerceivedWorld:
    def __init__(self):
        self.current_place = "womb"  # default prebirth anchor

    def observe(self, place: str):
        if place:
            self.current_place = place