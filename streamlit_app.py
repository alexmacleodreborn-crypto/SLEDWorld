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
# DEV / HARD RESET
# ==================================================
st.sidebar.header("Dev Controls")

if st.sidebar.button("🔄 HARD RESET WORLD"):
    st.session_state.clear()
    st.rerun()

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
    "Advance frames",
    min_value=1,
    max_value=50,
    value=5,
)

minutes_per_step = st.sidebar.slider(
    "Minutes per frame",
    min_value=1,
    max_value=60,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=minutes_per_step)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World (soft)"):
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
    "num_active_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------
# Observer View
# --------------------------
st.subheader("Observer Perception")

observer_found = False

for agent in world.agents:
    if hasattr(agent, "observe"):
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present in this world.")

# --------------------------
# Physical Agents (Walkers)
# --------------------------
st.subheader("Physical Agents")

for agent in world.agents:
    if hasattr(agent, "tick") and not hasattr(agent, "observe"):
        st.json(agent.snapshot())

# --------------------------
# Active Scouts (Focused Attention)
# --------------------------
st.subheader("Active Scouts")

scouts = getattr(world, "scouts", [])

if scouts:
    for scout in scouts:
        st.json(scout.snapshot())
else:
    st.write("No active scouts.")

# --------------------------
# Salience Investigator (Accounting Layer)
# --------------------------
st.subheader("Salience Investigator")

investigator = getattr(world, "salience_investigator", None)

if investigator is None:
    st.warning("Salience Investigator not present in this world instance.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.metric("Frames Processed", investigator.frame)
    st.metric("Ledger Entries", len(investigator.ledger))

with col2:
    st.json(investigator.snapshot())

# --------------------------
# Salience Ledger (Tail)
# --------------------------
st.subheader("Salience Ledger (Recent)")

if investigator.ledger:
    st.json(investigator.ledger[-10:])
else:
    st.write("No salience records yet.")

# ==================================================
# Footer
# ==================================================
st.caption(
    "World exists independently · "
    "Walkers cause change · "
    "Observers perceive · "
    "Scouts focus attention · "
    "Salience is accounted · "
    "Time is a coordinate, not a driver"
)