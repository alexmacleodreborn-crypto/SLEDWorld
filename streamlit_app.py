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

# 15 minutes of world time per UI refresh
clock.tick(0.25)

# Gestation / pre-birth / auto-birth logic
gestation.tick()

# -------------------------------------------------
# OBSERVER CONTROLS (NO BIOLOGY CONTROL)
# -------------------------------------------------

st.sidebar.header("Observer Control")

st.sidebar.write("World time always flows.")
st.sidebar.write("A7DO cannot be forced to wake or birth.")

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
# World state
# -------------------------

st.subheader("World Time")
st.json(clock.snapshot())

# -------------------------
# A7DO existence state
# -------------------------

st.subheader("A7DO State")
st.write(f"**Birthed:** {a7do.birthed}")
st.write(f"**Awake:** {a7do.is_awake}")
st.write(f"**Perceived Place:** {a7do.perceived_place}")

# -------------------------
# Internal log (observer-visible)
# -------------------------

st.subheader("Internal Log")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log[-30:]))
else:
    st.write("—")

# -------------------------
# Familiarity (pre-symbolic memory)
# -------------------------

st.subheader("Familiarity Patterns (Pre-Language)")
st.json(a7do.familiarity.top())

# -------------------------
# Body state (low-level autonomy)
# -------------------------

st.subheader("Body State")
st.json(a7do.body.snapshot())