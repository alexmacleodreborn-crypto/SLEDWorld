from collections import defaultdict
import random


class BodyState:
    """
    Physiological substrate.

    - No cognition
    - No symbols
    - No access to world time
    - Pre-birth capable
    - Stores repetition-based bodily memory
    """

    # ---------------------------------------------
    # Body segment map (numeric, pre-symbolic)
    # ---------------------------------------------
    SEGMENTS = {
        1: "head",
        2: "mouth",
        3: "left_hand",
        4: "right_hand",
        5: "left_arm",
        6: "right_arm",
        7: "torso",
        8: "left_leg",
        9: "right_leg",
    }

    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)

        # ---------------------------------------------
        # Core arousal state
        # ---------------------------------------------
        self.awake = False
        self.arousal = 0.1
        self.fatigue = 0.0

        # ---------------------------------------------
        # Movement + contact memory (pre-symbolic)
        # ---------------------------------------------
        self.motion_counts = defaultdict(int)
        self.contact_counts = defaultdict(int)

        self.last_motion = None          # segment id
        self.last_contact = None         # (seg_a, seg_b)

    # =================================================
    # BODY TRANSITIONS
    # =================================================

    def wake(self):
        self.awake = True
        self.arousal = min(1.0, self.arousal + 0.4)
        self.fatigue = max(0.0, self.fatigue - 0.2)

    def sleep(self):
        self.awake = False
        self.arousal = max(0.0, self.arousal - 0.3)
        self.fatigue = min(1.0, self.fatigue + 0.2)

    # =================================================
    # PHYSIOLOGICAL TICK
    # =================================================

    def tick(self):
        """
        Low-level body drift.
        """
        if self.awake:
            self.fatigue = min(1.0, self.fatigue + 0.01)
        else:
            self.fatigue = max(0.0, self.fatigue - 0.02)

    # =================================================
    # PRE-BIRTH / INFANT MOVEMENT
    # =================================================

    def spontaneous_motion(self):
        """
        Random limb movement.
        Pre-symbolic repetition generator.
        """
        seg = self.rng.choice(list(self.SEGMENTS.keys()))
        self.motion_counts[seg] += 1
        self.last_motion = seg
        return seg

    def spontaneous_contact(self):
        """
        Random body-to-body contact.
        e.g. hand → mouth, knee → torso.
        """
        a, b = self.rng.sample(list(self.SEGMENTS.keys()), 2)
        key = tuple(sorted((a, b)))
        self.contact_counts[key] += 1
        self.last_contact = key
        return key

    # =================================================
    # OBSERVER SNAPSHOT (JSON SAFE)
    # =================================================

    def snapshot(self):
        """
        Observer-only view.

        Converts tuple keys → strings
        WITHOUT altering internal representation.
        """

        contact_counts_serializable = {
            f"{a}-{b}": count
            for (a, b), count in self.contact_counts.items()
        }

        return {
            "awake": self.awake,
            "arousal": round(self.arousal, 3),
            "fatigue": round(self.fatigue, 3),

            "last_motion_segment": self.last_motion,
            "last_contact_segments": (
                f"{self.last_contact[0]}-{self.last_contact[1]}"
                if self.last_contact else None
            ),

            "motion_counts": dict(self.motion_counts),
            "contact_counts": contact_counts_serializable,
        }