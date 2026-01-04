import streamlit as st
from world_core.bootstrap import build_world

st.set_page_config(page_title="SLED World – World Core", layout="wide")

# -----------------------------
# Session init
# -----------------------------
if "world" not in st.session_state:
    st.session_state.world = build_world()

world = st.session_state.world

# -----------------------------
# Controls
# -----------------------------
st.sidebar.header("World Controls")

accel = st.sidebar.slider("Acceleration (world sec per real sec)", 1, 3600, 120, 1)
world["clock"].acceleration = accel

step_real_seconds = st.sidebar.selectbox("Tick step (real seconds)", [0.25, 0.5, 1.0, 2.0], index=2)

if st.sidebar.button("Tick once"):
    world.clock.tick(real_seconds=step_real_seconds)
    world["clock"].tick(real_seconds=step_real_seconds)

auto = st.sidebar.checkbox("Auto tick", value=True)

# -----------------------------
# Auto loop (safe/simple)
# -----------------------------
if auto:
    # Each rerun advances time by chosen step
    world["clock"].tick(real_seconds=step_real_seconds)
    world["clock"].tick(real_seconds=step_real_seconds)

# -----------------------------
# Display
# -----------------------------
st.title("SLED World – World Core (No A7DO)")

st.subheader("World Time")
st.json(world["clock"].snapshot())

st.subheader("Places")
for name, place in world["places"].items():
    st.write(f"### {name}")
    st.json(place.snapshot())

st.subheader("Agents")
st.json([a.snapshot() for a in world.agents])

st.caption("World Core only: time + places + agents. No A7DO, no gestation, no gating yet.")