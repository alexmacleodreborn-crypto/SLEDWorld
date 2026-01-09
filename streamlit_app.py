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
    max_value=10,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        # Advance time deliberately (minutes)
        clock.tick(minutes=1)

        # Advance world physics
        world.tick()

        # Let observers perceive
        for agent in world.agents:
            if hasattr(agent, "observe"):
                agent.observe(world)

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
# World State
# --------------------------
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
})

# --------------------------
# Observer View (PRIMARY)
# --------------------------
st.subheader("Observer Perception")

observer_found = False

for agent in world.agents:
    if hasattr(agent, "observe"):
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.error("No observation agent present.")

# --------------------------
# World Agents (Secondary)
# --------------------------
st.subheader("World Agents")

for agent in world.agents:
    st.json(agent.snapshot())

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality persists independently. "
    "Observers learn persistence. "
    "Time is subordinate."
)