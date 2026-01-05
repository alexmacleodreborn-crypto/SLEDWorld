import streamlit as st

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLED World – World Frame", layout="wide")

# =========================
# Session init
# =========================
if "world" not in st.session_state:
    st.session_state.world = build_world()

if "clock" not in st.session_state:
    # acceleration: how many WORLD seconds pass per REAL second (used when ticking by real_seconds)
    st.session_state.clock = WorldClock(acceleration=60)

world = st.session_state.world
clock = st.session_state.clock

# =========================
# Controls (button clock)
# =========================
st.sidebar.header("World Clock Controls")

accel = st.sidebar.slider("Acceleration (world seconds per real second)", 1, 3600, int(clock.acceleration))
clock.acceleration = accel  # ✅ FIX: clock is separate, not world.clock

step_minutes = st.sidebar.selectbox("Step size", [1, 5, 15, 30, 60, 180, 720, 1440], index=2)

colA, colB = st.sidebar.columns(2)
with colA:
    if st.button("Tick +1 step"):
        clock.tick(minutes=step_minutes)

with colB:
    if st.button("Tick +10 steps"):
        clock.tick(minutes=step_minutes * 10)

st.sidebar.divider()

real_seconds = st.sidebar.slider("Auto step (real seconds)", 0.0, 5.0, 0.0, 0.1)
if real_seconds > 0:
    # This advances world time continuously based on real time pacing
    clock.tick(real_seconds=real_seconds)

# =========================
# Display
# =========================
st.title("SLED World – World Frame")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("World Places")
# WorldState holds places in world.places
for name, place in world.places.items():
    with st.expander(name, expanded=False):
        st.json(place.snapshot())