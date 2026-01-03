import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot
from a7do_core.experience_event import ExperienceEvent
from a7do_core.event_applier import apply_event

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# -------------------------
# Session init
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot()

a7do = st.session_state.a7do
cycle = st.session_state.cycle
clock = st.session_state.clock
mother = st.session_state.mother

# -------------------------
# World tick
# -------------------------

clock.tick(0.25)

# -------------------------
# Prebirth sensory drip
# -------------------------

if not a7do.birthed and a7do.is_awake:
    drip = mother.sensory_output(prebirth=True)
    ev = ExperienceEvent(
        place="womb",
        channels=drip,
        intensity=0.4
    )
    apply_event(a7do, ev)

# -------------------------
# Controls
# -------------------------

st.sidebar.header("Observer Control")

if not cycle.has_birthed:
    if st.sidebar.button("Trigger Birth"):
        cycle.ensure_birth()
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

# -------------------------
# Display
# -------------------------

st.title("A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("A7DO State")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perceived place:", a7do.perceived_place)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")

st.subheader("Familiarity Patterns")
st.json(a7do.familiarity.top())