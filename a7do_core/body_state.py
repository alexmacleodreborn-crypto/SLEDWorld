from collections import defaultdict
import random


class BodyState:
    """
    Pre-symbolic physiological substrate.

    DESIGN PRINCIPLES
    -----------------
    - No language
    - No concepts
    - No world awareness
    - No time awareness
    - Stores ONLY movement, contact, pressure patterns

    All body parts are indexed numerically.
    Names exist ONLY for observer mapping.
    """

    def __init__(self):
        # ---------------------------------------------
        # Arousal state (pure physiology)
        # ---------------------------------------------
        self.awake = False
        self.arousal = 0.1
        self.fatigue = 0.0

        # ---------------------------------------------
        # Body segments (index → observer label)
        # ---------------------------------------------
        self.segments = {
            0: "head",
            1: "torso",
            2: "left_arm",
            3: "left_hand",
            4: "right_arm",
            5: "right_hand",
            6: "left_leg",
            7: "right_leg",
            8: "mouth",
            9: "fingers",
            10: "feet",
        }

        # ---------------------------------------------
        # Local non-cognitive memory
        # ---------------------------------------------
        self.motion_counts = defaultdict(int)     # seg_index → count
        self.contact_counts = defaultdict(int)    # "a-b" → count

        # Last detected activity (observer only)
        self.last_motion = None                   # seg_index
        self.last_contact = None                  # "a-b"

        # Random source for organic movement
        self.rng = random.Random(42)

    # =================================================
    # BODY STATE TRANSITIONS
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
    # PRE-BIRTH / INFANT BODY ACTIVITY
    # =================================================

    def spontaneous_movement(self):
        """
        Random micro-movement.
        Represents kicking, stretching, twitching.
        """
        seg = self.rng.choice(list(self.segments.keys()))
        self.motion_counts[seg] += 1
        self.last_motion = seg

    def contact(self, seg_a: int, seg_b: int):
        """
        Records self-contact (e.g. hand-to-mouth).
        Uses STRING key to remain JSON-safe.
        """
        if seg_a == seg_b:
            return

        a, b = sorted((seg_a, seg_b))
        key = f"{a}-{b}"

        self.contact_counts[key] += 1
        self.last_contact = key

    def tick(self):
        """
        Body tick.
        Runs regardless of awareness or phase.
        """

        # Fatigue dynamics
        if self.awake:
            self.fatigue = min(1.0, self.fatigue + 0.01)
        else:
            self.fatigue = max(0.0, self.fatigue - 0.02)

        # Spontaneous motion (pre-birth heavy)
        if self.rng.random() < 0.3:
            self.spontaneous_movement()

        # Self-contact (thumb sucking, foot touching)
        if self.rng.random() < 0.1:
            a = self.rng.choice(list(self.segments.keys()))
            b = self.rng.choice(list(self.segments.keys()))
            self.contact(a, b)

    # =================================================
    # OBSERVER SNAPSHOT (JSON SAFE)
    # =================================================

    def snapshot(self):
        """
        Observer-only representation.
        Fully JSON serialisable.
        """
        return {
            "awake": self.awake,
            "arousal": round(self.arousal, 3),
            "fatigue": round(self.fatigue, 3),

            "last_motion_segment": self.last_motion,
            "last_motion_label": (
                self.segments.get(self.last_motion)
                if self.last_motion is not None else None
            ),

            "last_contact": self.last_contact,

            "motion_counts": dict(self.motion_counts),
            "contact_counts": dict(self.contact_counts),
        }