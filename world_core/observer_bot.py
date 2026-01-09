class ObserverBot:
    """
    Passive observer.
    Does not move.
    Does not act.
    Does not depend on clock.
    Only records what persists in the world.
    """

    def __init__(self, name="observer"):
        self.name = name
        self.seen_places = {}
        self.frames_observed = 0

    def observe(self, world):
        """
        Observe the world without changing it.
        """
        self.frames_observed += 1

        for place_name in world.places.keys():
            self.seen_places.setdefault(place_name, 0)
            self.seen_places[place_name] += 1

# world_core/salience_investigator_bot.py

from collections import defaultdict
from typing import Dict, List, Any


class SalienceInvestigatorBot:
    """
    Salience Investigator (Accounting Layer)

    Role:
    - Receives observer reports
    - Converts observations into transaction records
    - Accumulates structural salience
    - NO cognition
    - NO decisions
    - NO feedback into world

    This bot builds the *infrastructure of mind*,
    not thoughts themselves.
    """

    def __init__(self, name: str = "Salience-Investigator"):
        self.name = name

        # -------------------------------------------------
        # Transaction ledger (append-only)
        # -------------------------------------------------
        self.ledger: List[Dict[str, Any]] = []

        # -------------------------------------------------
        # Structural accumulation indexes
        # -------------------------------------------------
        self.entity_exposure = defaultdict(int)
        self.place_exposure = defaultdict(int)
        self.frame_counter = 0

    # =================================================
    # INGESTION (Observer → Investigator)
    # =================================================

    def ingest_observer_snapshot(self, snapshot: Dict[str, Any]):
        """
        Receives a snapshot from ObserverBot.
        Converts perception into transactions.
        """

        self.frame_counter += 1

        observer_name = snapshot.get("name", "unknown_observer")

        # -------------------------
        # Seen places
        # -------------------------
        seen_places = snapshot.get("seen_places", {})

        for place_name, count in seen_places.items():
            transaction = self._build_transaction(
                entity_type="place",
                entity_name=place_name,
                exposure=count,
                observer=observer_name,
            )

            self.ledger.append(transaction)
            self.place_exposure[place_name] += 1

    # =================================================
    # TRANSACTION BUILDER
    # =================================================

    def _build_transaction(
        self,
        entity_type: str,
        entity_name: str,
        exposure: int,
        observer: str,
    ) -> Dict[str, Any]:
        """
        Constructs a single salience transaction.
        """

        tags = self._derive_tags(entity_type, exposure)

        return {
            "frame": self.frame_counter,          # coordinate, not time
            "observer": observer,

            "entity": {
                "type": entity_type,
                "name": entity_name,
            },

            "metrics": {
                "exposure": exposure,
            },

            "tags": tags,
        }

    # =================================================
    # TAG DERIVATION (NON-COGNITIVE)
    # =================================================

    def _derive_tags(self, entity_type: str, exposure: int) -> List[str]:
        """
        Assigns structural tags only.
        No meaning. No interpretation.
        """

        tags = [entity_type]

        if exposure > 5:
            tags.append("recurrent")
        else:
            tags.append("rare")

        if entity_type == "place":
            tags.append("spatial")
            tags.append("static")

        return tags

    # =================================================
    # OBSERVER VIEW
    # =================================================

    def snapshot(self) -> Dict[str, Any]:
        """
        Observer-safe snapshot.
        No internal reasoning exposed.
        """

        return {
            "name": self.name,
            "frames_processed": self.frame_counter,
            "total_transactions": len(self.ledger),
            "known_places": dict(self.place_exposure),
        }

    def snapshot(self):
        """
        Return observer memory.
        """
        return {
            "name": self.name,
            "frames_observed": self.frames_observed,
            "seen_places": dict(self.seen_places),
        }