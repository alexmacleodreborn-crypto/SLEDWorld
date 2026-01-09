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
# HARD RESET (DEV SAFETY)
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
    "num_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------
# Observer Perception
# --------------------------
st.subheader("Observer Perception")

observer_found = False
for agent in world.agents:
    if hasattr(agent, "observe") and hasattr(agent, "snapshot"):
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present in this world.")

# --------------------------
# Physical Agents (Walkers)
# --------------------------
st.subheader("Physical Agents")

for agent in world.agents:
    if hasattr(agent, "tick") and hasattr(agent, "snapshot") and not hasattr(agent, "observe"):
        st.json(agent.snapshot())

# --------------------------
# Scouts (Focused Attention)
# --------------------------
st.subheader("Scouts (Focused Attention)")

scouts = getattr(world, "scouts", [])

if not scouts:
    st.write("No active scouts.")
else:
    for scout in scouts:
        st.json(scout.snapshot())

# ==================================================
# Salience Investigator (STATE BINDING)
# ==================================================
st.subheader("Salience Investigator — State Binding")

investigator = getattr(world, "salience_investigator", None)

if investigator is None:
    st.warning("Salience Investigator not present in this world instance.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.metric("Frames Processed", investigator.frame)
    st.metric("Known Shapes", len(investigator.shape_memory))

with col2:
    st.metric("State Events", len(investigator.ledger))

st.json(investigator.snapshot())

# ==================================================
# Emergent State Transitions (STEP 2)
# ==================================================
st.subheader("Emergent State Transitions (Pre-Language)")

if not investigator.ledger:
    st.write("No state transitions detected yet.")
else:
    for event in investigator.ledger[-10:]:
        direction = event["direction"]
        color = "🟢" if direction == "up" else "🔴"

        st.markdown(
            f"""
            {color} **Frame {event['frame']}**  
            Shape: `{event['shape_id']}`  
            ΔSound: {event['state_delta']['sound']}  
            ΔLight: {event['state_delta']['light']}  
            Persistence: {event['persistence']}
            """
        )

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists independently · "
    "Walkers cause change · "
    "Observers perceive · "
    "Scouts bind structure · "
    "States emerge before language · "
    "Time is a coordinate, not a driver"
)