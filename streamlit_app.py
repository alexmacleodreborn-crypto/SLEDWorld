import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# -------------------------
# Session init
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
clock = st.session_state.clock
gestation = st.session_state.gestation
cycle = st.session_state.cycle

# -------------------------
# WORLD TICK (REAL TIME)
# -------------------------

clock.tick()
gestation.tick(clock)

if not a7do.birthed and gestation.ready_for_birth():
    cycle.ensure_birth()
    gestation.mark_completed()
    a7do.internal_log.append("auto-birth: gestation threshold reached")

# -------------------------
# Controls (post-birth)
# -------------------------

st.sidebar.header("Observer")

if a7do.birthed:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.day += 1

# -------------------------
# Display
# -------------------------

st.title("A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("Gestation")
st.write("Elapsed days:", round(gestation.elapsed_days, 2))
st.write("Ready:", gestation.ready_for_birth())

st.subheader("A7DO State")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perceived place:", a7do.perceived_place)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log[-20:]) if a7do.internal_log else "—")

st.subheader("Familiarity")
st.json(a7do.familiarity.top())

# -------------------------
# AUTO REFRESH (ESSENTIAL)
# -------------------------

st.caption("⏱ World runs on real time. Refresh page or interact to advance.")