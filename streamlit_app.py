import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
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

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
clock = st.session_state.clock
gestation = st.session_state.gestation
cycle = st.session_state.cycle

# -------------------------
# World tick (always runs)
# -------------------------

clock.tick(0.25)  # 15 minutes per UI refresh

# -------------------------
# Gestation → Birth (AUTOMATIC)
# -------------------------

if not a7do.birthed:
    gestation.tick(clock)

    if gestation.ready_for_birth():
        cycle.ensure_birth()
        a7do.internal_log.append(
            "transition: gestation complete → birth event"
        )

# -------------------------
# Observer controls (post-birth only)
# -------------------------

st.sidebar.header("Observer Control")

if a7do.birthed:
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

st.subheader("Gestation")
st.write("Elapsed days:", round(gestation.elapsed_days, 2))
st.write("Ready for birth:", gestation.ready_for_birth())

st.subheader("A7DO State")
st.write("Awake:", a7do.is_awake)
st.write("Birthed:", a7do.birthed)
st.write("Perceived place:", a7do.perceived_place)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")

st.subheader("Familiarity Patterns (pre-symbolic)")
st.json(a7do.familiarity.top())