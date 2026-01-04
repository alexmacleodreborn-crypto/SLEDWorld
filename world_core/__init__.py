# world_core/__init__.py

"""
world_core

Objective world simulation:
- Time
- Physics
- Agents (MotherBot, later others)
- No cognition
- No subjective state
"""

from .world_clock import WorldClock
from .mother_bot import MotherBot
from .heartbeat_field import HeartbeatField


