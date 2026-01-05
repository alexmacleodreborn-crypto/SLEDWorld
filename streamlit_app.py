import streamlit as st

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

# ==================================================
# Streamlit config
# ==================================================
st.set_page_config(
    page_title="SLED World – World Frame",
    layout="wide"
)

# ==================================================
# Session initialisation (ORDER MATTERS)
# ==================================================
if "clock" not in st.session_state:
    # acceleration = WORLD seconds per REAL second
    st.session_state.clock = WorldClock(acceleration=60)

clock = st.session_state.clock

if "world" not in st.session_state:
    # ✅ FIX: pass clock into build_world
    st.session_state.world = build_world(clock)

world = st.session_state.world

# ==================================================
# Sidebar – World Clock Controls
# ==================================================
st.sidebar.header("World Clock Controls")

accel = st.sidebar.slider(
    "Acceleration (world seconds per real second)",
    min_value=1,
    max_value=3600,
    value=int(clock.acceleration),
)
clock.acceleration = accel

step_minutes = st.sidebar.selectbox(
    "Step size (minutes)",
    [1, 5, 15, 30, 60, 180, 720, 1440],
    index=2
)

colA, colB = st.sidebar.columns(2)

with colA:
    if st.button("Tick +1 step"):
        clock.tick(minutes=step_minutes)
        world.tick(clock)

with colB:
    if st.button("Tick +10 steps"):
        clock.tick(minutes=step_minutes * 10)
        world.tick(clock)

st.sidebar.divider()

real_seconds = st.sidebar.slider(
    "Auto step (real seconds)",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

if real_seconds > 0:
    clock.tick(real_seconds=real_seconds)
    world.tick()

# ==================================================
# Main Display
# ==================================================
st.title("SLED World – World Frame")

# --------------------------
# World Time
# --------------------------
st.subheader("World Time")
st.json(clock.snapshot())

st.caption(
    f"World clock running at {clock.acceleration}× real time · "
    f"Step size: {step_minutes} minutes"
)

# --------------------------
# World Grid
# --------------------------
st.subheader("World Grid")
st.json(world.grid.snapshot())

# --------------------------
# World Summary
# --------------------------
st.subheader("World Summary")
st.json({
    "num_places": len(world.places),
    "place_names": list(world.places.keys()),
    "num_agents": len(world.agents),
})

# --------------------------
# World Places
# --------------------------
st.subheader("World Places")

for name, place in world.places.items():
    with st.expander(name, expanded=False):
        st.json(place.snapshot())

# --------------------------
# World Agents (NOW LIVE)
# --------------------------
st.subheader("World Agents")

if not world.agents:
    st.write("No active agents.")
else:
    for agent in world.agents:
        st.json(agent.snapshot())

# ==================================================
# Footer
# ==================================================
st.caption(
    "This view represents the objective world frame. "
    "Agents move according to world time, not perception."
)