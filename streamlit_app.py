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
# Session initialisation
# ==================================================
if "world" not in st.session_state:
    st.session_state.world = build_world()

if "clock" not in st.session_state:
    # acceleration = WORLD seconds per REAL second
    st.session_state.clock = WorldClock(acceleration=60)

world = st.session_state.world
clock = st.session_state.clock

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
clock.acceleration = accel  # clock is independent of world (intentional)

step_minutes = st.sidebar.selectbox(
    "Step size (minutes)",
    [1, 5, 15, 30, 60, 180, 720, 1440],
    index=2
)

colA, colB = st.sidebar.columns(2)

with colA:
    if st.button("Tick +1 step"):
        clock.tick(minutes=step_minutes)

with colB:
    if st.button("Tick +10 steps"):
        clock.tick(minutes=step_minutes * 10)

st.sidebar.divider()

real_seconds = st.sidebar.slider(
    "Auto step (real seconds)",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

if real_seconds > 0:
    # Continuous time advance (observer-controlled)
    clock.tick(real_seconds=real_seconds)

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
# World Summary (NEW – SAFE)
# --------------------------
st.subheader("World Summary")
st.json({
    "num_places": len(world.places),
    "place_names": list(world.places.keys()),
})

# --------------------------
# World Places
# --------------------------
st.subheader("World Places")

for name, place in world.places.items():
    with st.expander(name, expanded=False):
        st.json(place.snapshot())

# --------------------------
# World Agents (placeholder)
# --------------------------
st.subheader("World Agents")
st.write("No active agents loaded in world frame.")

# ==================================================
# Footer
# ==================================================
st.caption(
    "This view represents the objective world frame. "
    "No cognitive agents perceive this layer directly."
)