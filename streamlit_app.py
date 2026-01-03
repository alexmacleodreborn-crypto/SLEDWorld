import time
import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide"
)

# =========================================================
# Session initialisation
# =========================================================

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()

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

# =========================================================
# WORLD TICK (REAL TIME → WORLD TIME)
# =========================================================

now = time.time()
delta = now - st.session_state.last_tick

# advance world every ~1 second
if delta >= 1.0:
    st.session_state.last_tick = now

    # world time moves
    clock.tick()

    # gestation progresses automatically
    gestation.tick()

    # force Streamlit to rerun (THIS is the refresh)
    st.experimental_rerun()

# =========================================================
# UI
# =========================================================

st.title("🧠 SLED World – A7DO Cognitive Emergence")

st.subheader("🌍 World Time")
st.json(clock.snapshot())

st.subheader("🤰 Gestation")
st.write("Completed:", gestation.completed)
st.write("Gestation days:", round(clock.days_elapsed, 2))

st.subheader("👩 Mother (World Entity)")
st.json(mother.snapshot(clock.world_minutes))

st.subheader("👶 A7DO Body (Internal)")
st.json(a7do.body.snapshot(clock.world_minutes))

st.subheader("🧠 Familiarity Patterns")
st.json(a7do.familiarity.patterns)

st.subheader("📜 Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")