import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# -------------------------------------------------
# Session initialisation
# -------------------------------------------------

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        clock=st.session_state.clock,
    )

clock = st.session_state.clock
a7do = st.session_state.a7do
cycle = st.session_state.cycle
gestation = st.session_state.gestation

# -------------------------------------------------
# WORLD TICK (ALWAYS RUNNING)
# -------------------------------------------------

clock.tick(minutes=15)

# Pre-birth automatic experience
if not a7do.birthed:
    gestation.tick()

# -------------------------------------------------
# Observer Controls (POST-BIRTH ONLY)
# -------------------------------------------------

st.sidebar.header("Observer Control")

if a7do.birthed:
    if not a7do.is_awake:
        if st.sidebar.button("Wake"):
            cycle.wake()
    else:
        if st.sidebar.button("Sleep"):
            cycle.sleep()
            cycle.next_day()

# -------------------------------------------------
# DISPLAY
# -------------------------------------------------

st.title("SLED World – A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("A7DO State")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perceived Place:", a7do.perceived_place)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log[-25:]) if a7do.internal_log else "—")

st.subheader("Familiarity Patterns (Pre-symbolic)")
st.json(a7do.familiarity.top())

st.subheader("Body Snapshot")
st.json(a7do.body.snapshot())