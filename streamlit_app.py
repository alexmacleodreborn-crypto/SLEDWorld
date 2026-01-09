# streamlit_app.py

import streamlit as st

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

# ==================================================
# Streamlit config
# ==================================================
st.set_page_config(
    page_title="SLEDWorld – Reality Frame",
    layout="wide"
)

# ==================================================
# Session initialisation
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# ==================================================
# Sidebar – World Advancement
# ==================================================
st.sidebar.header("World Advancement")

advance_steps = st.sidebar.slider(
    "Advance steps",
    min_value=1,
    max_value=20,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

# ==================================================
# Main Display
# ==================================================
st.title("SLEDWorld – Reality Frame")

# --------------------------
# World Summary
# --------------------------
st.subheader("World State")

st.json({
    "frame": world.frame,
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------
# Geometry & Places
# --------------------------
st.subheader("World Geometry")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json(place.snapshot())

# --------------------------
# Observer View
# --------------------------
st.subheader("Observer Perception")

observer_found = False
for agent in world.agents:
    if agent.__class__.__name__ == "ObserverBot":
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present.")

# --------------------------
# All Agents
# --------------------------
st.subheader("World Agents")

for agent in world.agents:
    if hasattr(agent, "snapshot"):
        st.json(agent.snapshot())

# --------------------------
# Scouts
# --------------------------
st.subheader("Active Scouts")

if world.scouts:
    for scout in world.scouts:
        st.json(scout.snapshot())
else:
    st.write("No active scouts.")

# --------------------------
# Salience Ledger
# --------------------------
st.subheader("Salience Ledger")

ledger = world.salience_investigator

st.metric("Ledger Entries", len(ledger.ledger))

st.json(ledger.snapshot())

st.subheader("Recent Transactions")
st.json(ledger.ledger[-10:])

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Motion causes change. "
    "Perception detects. "
    "Salience stabilises. "
    "Meaning emerges."
)