from dataclasses import dataclass

from world_core.mother_bot import MotherBot
from a7do_core.event_applier import apply_event


@dataclass
class GestationBridge:
    """
    Bridges world-time maternal signals into A7DO pre-birth experience.
    A7DO does NOT control this.
    """
    a7do: object
    clock: object

    mother: MotherBot = MotherBot()
    gestation_days: int = 270
    elapsed_days: float = 0.0
    completed: bool = False

    def tick(self):
        """
        Called every world tick.
        Feeds muted sensory patterns to A7DO until birth threshold.
        """
        if self.completed:
            return

        # Advance mother independently
        self.mother.tick(minutes=15)

        # Advance gestation time
        self.elapsed_days = self.clock.days_elapsed

        # Pre-birth sensory exposure
        snapshot = self.mother.prebirth_sensory_snapshot()
        apply_event(self.a7do, snapshot)

        # Birth trigger (automatic, not button-driven)
        if self.elapsed_days >= self.gestation_days:
            self.completed = True
            self.a7do.mark_birthed()
            self.a7do.unlock_awareness()
            self.a7do.internal_log.append(
                "birth: transition from womb to external world"
            )