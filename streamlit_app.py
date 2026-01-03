import streamlit as st

from world_core.world_bootstrap import bootstrap_world
from world_core.world_clock import WorldClock
from experience_layer.event_generator import generate_event
from a7do_core.a7do_state import A7DOState
from a7do_core.event_applier import apply_event

st.set_page_config(page_title="SLED World", layout="wide")

if "world" not in st.session_state:
    st.session_state.world = bootstrap_world()
    st.session_state.clock = WorldClock(st.session_state.world)
    st.session_state.a7do = A7DOState()

world = st.session_state.world
a7do = st.session_state.a7do
clock = st.session_state.clock

st.title("🌍 SLED World")

st.sidebar.header("Observer Control")

if st.sidebar.button("Run Birth Experience"):
    ev = generate_event(world, "hospital")
    apply_event(a7do, ev)

if st.sidebar.button("Advance 6 Hours"):
    clock.advance(6)

if st.sidebar.button("Sleep"):
    a7do.sleep()

st.subheader("World State")
st.json({
    "day": world.day,
    "time": world.time_of_day,
    "bots": {k: v.location for k, v in world.bots.items()},
})

st.subheader("A7DO Internal Log")
st.write(a7do.internal_log)