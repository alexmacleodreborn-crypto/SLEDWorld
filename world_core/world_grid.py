# world_core/world_grid.py

from __future__ import annotations
from typing import Dict, Any

class WorldGrid:
    """
    Registry of objects in world space.
    """
    def __init__(self):
        self.registry: Dict[str, Any] = {}

    def register(self, obj) -> None:
        self.registry[obj.name] = obj

    def snapshot(self):
        return {
            "registered": list(self.registry.keys())
        }