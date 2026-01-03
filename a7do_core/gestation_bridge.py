from dataclasses import dataclass

@dataclass
class GestationBridge:
    gestation_days_required: float = 180.0
    elapsed_days: float = 0.0
    completed: bool = False

    def tick(self, clock):
        self.elapsed_days = clock.days_elapsed

    def ready_for_birth(self) -> bool:
        return (not self.completed) and self.elapsed_days >= self.gestation_days_required

    def mark_completed(self):
        self.completed = True