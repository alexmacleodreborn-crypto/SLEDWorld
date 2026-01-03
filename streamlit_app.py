import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# -------------------------
# Session initialisation
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
clock = st.session_state.clock
cycle = st.session_state.cycle

# -------------------------
# World tick (always runs)
# -------------------------

clock.tick(0.25)  # 15 minutes per UI refresh

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
st.write("Awake:", a7do.is_awake)
st.write("Birthed:", a7do.birthed)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")

st.subheader("Familiarity Patterns")
st.json(a7do.familiarity.top())