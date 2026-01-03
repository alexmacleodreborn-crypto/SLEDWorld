import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock

# -------------------------------------------------
# Streamlit setup
# -------------------------------------------------

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

# 🔁 Auto-refresh: keeps world time running
# 1000 ms = 1 second real time
st.autorefresh(interval=1000, key="world_tick")

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
# WORLD TICK (always runs)
# -------------------------------------------------

# Each UI refresh advances world time
# 0.25 hours = 15 world minutes
clock.tick(0.25)

# Pre-birth / gestation / auto-birth bridge
gestation.tick()

# Passive body decay (always safe)
a7do.body.tick()

# -------------------------------------------------
# OBSERVER CONTROLS (NON-BIOLOGICAL)
# -------------------------------------------------

st.sidebar.header("Observer Control")

st.sidebar.write("• World time always runs")
st.sidebar.write("• Biology cannot be forced")

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

# -------------------------
# World time
# -------------------------

st.subheader("World Time")
st.json(clock.snapshot())

# -------------------------
# A7DO state
# -------------------------

st.subheader("A7DO State")
st.write("**Birthed:**", a7do.birthed)
st.write("**Awake:**", a7do.is_awake)
st.write("**Perceived Place:**", a7do.perceived_place)

# -------------------------
# Internal log (observer-visible)
# -------------------------

st.subheader("Internal Log")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log[-40:]))
else:
    st.write("—")

# -------------------------
# Familiarity (pre-symbolic memory)
# -------------------------

st.subheader("Familiarity Patterns (Pre-Language)")
st.json(a7do.familiarity.top())

# -------------------------
# Body state (somatic layer)
# -------------------------

st.subheader("Body State")
st.json(a7do.body.snapshot())