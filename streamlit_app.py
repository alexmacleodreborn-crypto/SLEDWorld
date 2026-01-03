import streamlit as st
import time

from world_core.world_bootstrap import bootstrap_world
from world_core.world_clock import WorldClock
from experience_layer.event_generator import generate_event
from experience_layer.sensory_drip import sensory_drip
from a7do_core.a7do_state import A7DOState
from a7do_core.event_applier import apply_event


st.set_page_config(page_title="SLED World", layout="wide")


# -----------------------------
# Session state initialisation
# -----------------------------
if "world" not in st.session_state:
    st.session_state.world = bootstrap_world()
    st.session_state.clock = WorldClock(st.session_state.world)
    st.session_state.a7do = A7DOState()

# 🔒 ALWAYS bind locals AFTER session init
world = st.session_state.world
clock = st.session_state.clock
a7do = st.session_state.a7do


# -----------------------------
# UI
# -----------------------------
st.title("🌍 SLED World")

st.sidebar.header("Observer Control")

if st.sidebar.button("Run Birth Experience"):
    ev = generate_event(world, "hospital")
    apply_event(a7do, ev)
    a7do.mark_birth()

if st.sidebar.button("Sleep"):
    a7do.sleep()

if st.sidebar.button("Wake"):
    a7do.wake()


# -----------------------------
# Continuous sensory drip
# -----------------------------
if a7do.is_awake:
    clock.advance(0.25)  # 15 min world time
    drip = sensory_drip(
        world,
        "hospital" if not a7do.birthed else "home"
    )
    apply_event(a7do, drip)
    time.sleep(0.5)


# -----------------------------
# Display
# -----------------------------
st.subheader("World State")
st.json({
    "day": world.day,
    "time": world.time_of_day,
    "bots": {k: v.location for k, v in world.bots.items()},
})

st.subheader("A7DO Internal Log")
st.write(a7do.internal_log)