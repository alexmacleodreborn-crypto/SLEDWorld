from collections import defaultdict
import random


class BodyState:
    """
    Pre-symbolic physiological substrate.

    - No language
    - No concepts
    - No world awareness
    - Stores only movement, contact, pressure patterns
    """

    def __init__(self):
        # ---------------------------------------------
        # Arousal state
        # ---------------------------------------------
        self.awake = False
        self.arousal = 0.1
        self.fatigue = 0.0

        # ---------------------------------------------
        # Body segments (indexed, not named)
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
        # Local body memory (non-cognitive)
        # ---------------------------------------------
        self.motion_counts = defaultdict(int)
        self.contact_counts = defaultdict(int)

        # Last detected activity (observer only)
        self.last_motion = None
        self.last_contact = None

        # Random source for micro-movements
        self.rng = random.Random(42)

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
    # PRE-BIRTH / INFANT BODY ACTIVITY
    # =================================================

    def spontaneous_movement(self):
        """
        Generates random low-level body movement.
        Pre-birth and infant-safe.
        """
        seg = self.rng.choice(list(self.segments.keys()))
        self.motion_counts[seg] += 1
        self.last_motion = seg

    def contact(self, seg_a: int, seg_b: int):
        """
        Records contact between two body segments.
        """
        key = tuple(sorted((seg_a, seg_b)))
        self.contact_counts[key] += 1
        self.last_contact = key

    def tick(self):
        """
        Body tick.
        Runs regardless of awareness.
        """
        # Fatigue dynamics
        if self.awake:
            self.fatigue = min(1.0, self.fatigue + 0.01)
        else:
            self.fatigue = max(0.0, self.fatigue - 0.02)

        # Spontaneous motion (more frequent pre-birth)
        if self.rng.random() < 0.3:
            self.spontaneous_movement()

        # Self-contact (e.g. hand to mouth)
        if self.rng.random() < 0.1:
            a = self.rng.choice(list(self.segments.keys()))
            b = self.rng.choice(list(self.segments.keys()))
            if a != b:
                self.contact(a, b)

    # =================================================
    # OBSERVER SNAPSHOT
    # =================================================

    def snapshot(self):
        return {
            "awake": self.awake,
            "arousal": round(self.arousal, 3),
            "fatigue": round(self.fatigue, 3),
            "last_motion_segment": self.last_motion,
            "last_contact_segments": self.last_contact,
            "motion_counts": dict(self.motion_counts),
            "contact_counts": dict(self.contact_counts),
        }