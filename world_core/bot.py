from dataclasses import dataclass

@dataclass
class Bot:
    name: str
    role: str  # mum, dad, nurse, neighbour
    location: str
    routine: str = "idle"

    def move_to(self, place: str):
        self.location = place