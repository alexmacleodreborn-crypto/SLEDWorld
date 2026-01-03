import streamlit as st
import time

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock

# -------------------------------------------------
# Safe rerun (works across Streamlit versions)
# -------------------------------------------------

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        # Last-resort fallback: trigger state change
        st.session_state["_rerun"] = time.time()

# -------------------------------------------------
# Streamlit setup
# -------------------------------------------------

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

# -------------------------------------------------
# Session initialisation (ONCE)
# -------------------------------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        st.session_state.a7do,
        st.session_state.clock,
    )

a7do = st.session_state.a7do
clock = st.session_state.clock
cycle = st.session_state.cycle
gestation = st.session_state.gestation

# -------------------------------------------------
# WORLD TICK (ALWAYS RUNS)
# -------------------------------------------------

# Advance world time
clock.tick(0.25)  # 15 minutes per UI cycle

# Pre-birth gestation & auto-birth
gestation.tick()

# Passive body decay
a7do.body.tick()

# -------------------------------------------------
# OBSERVER CONTROLS
# -------------------------------------------------

st.sidebar.header("Observer Control")

if a7do.birthed:
    if not a7do.is_awake:
        if st.sidebar.button("Wake A7DO"):
            cycle.wake()
    else:
        if st.sidebar.button("Sleep A7DO"):
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
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log[-40:]))
else:
    st.write("—")

st.subheader("Familiarity Patterns")
st.json(a7do.familiarity.top())

st.subheader("Body State")
st.json(a7do.body.snapshot())

# -------------------------------------------------
# 🔁 GUARANTEED WORLD LOOP
# -------------------------------------------------

time.sleep(1)
safe_rerun()