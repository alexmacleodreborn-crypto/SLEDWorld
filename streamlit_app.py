import streamlit as st
from streamlit_autorefresh import st_autorefresh

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_core.world_clock import WorldClock

st.set_page_config(
    page_title="SLED World – A7DO",
    layout="wide",
)

# ---------------------------------
# 🔁 FORCE PERIODIC RERUN (TIME)
# ---------------------------------
st_autorefresh(interval=1000, key="world_tick")  # every 1 second

# ---------------------------------
# Session initialisation
# ---------------------------------

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

# ---------------------------------
# ⏱ WORLD TIME TICK (ALWAYS RUNS)
# ---------------------------------
clock.tick(minutes=15)

# ---------------------------------
# Observer Controls
# ---------------------------------

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

# ---------------------------------
# DISPLAY
# ---------------------------------

st.title("A7DO – Pre-Symbolic Emergence")

st.subheader("World Time (Always Running)")
st.json(clock.snapshot())

st.subheader("A7DO State")
st.write("Awake:", a7do.is_awake)
st.write("Birthed:", a7do.birthed)

st.subheader("Body Autonomy (Pre-Intentional)")
st.json(a7do.body_snapshot())

st.subheader("Sensory Familiarity (Gated)")
st.json(a7do.familiarity_snapshot())

st.subheader("Last Sleep Replay")
st.write(cycle.last_sleep_replay() or "—")

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")