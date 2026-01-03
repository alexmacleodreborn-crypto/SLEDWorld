import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide"
)

# Auto refresh every second (REQUIRED)
st.autorefresh(interval=1000, key="world_tick")

# -------------------------
# Session init
# -------------------------

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration_minutes_per_second=15)

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
        clock=st.session_state.clock,
    )

clock = st.session_state.clock
mother = st.session_state.mother
a7do = st.session_state.a7do
gestation = st.session_state.gestation

# -------------------------
# World tick (ALWAYS)
# -------------------------

clock.tick()
gestation.tick()

# -------------------------
# UI
# -------------------------

st.title("SLED World – A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("Gestation")
st.write("Completed:", gestation.completed)

st.subheader("Mother")
st.json(mother.snapshot(clock.world_minutes))

st.subheader("A7DO Body")
st.json(a7do.body.snapshot(clock.world_minutes))

st.subheader("Familiarity (top patterns)")
st.json(a7do.familiarity.patterns)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")