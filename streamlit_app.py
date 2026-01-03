import streamlit as st

# ==============================
# Core imports
# ==============================

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot


# ==============================
# Streamlit config
# ==============================

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)


# ==============================
# Session initialisation
# ==============================

if "clock" not in st.session_state:
    clock = WorldClock(acceleration=60)  # 1 real sec = 60 world seconds
    clock.start()
    st.session_state.clock = clock

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot(st.session_state.clock)

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
        clock=st.session_state.clock,
    )

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)


# ==============================
# Aliases
# ==============================

clock = st.session_state.clock
a7do = st.session_state.a7do
mother = st.session_state.mother
gestation = st.session_state.gestation
cycle = st.session_state.cycle


# ==============================
# WORLD TICK (always runs)
# ==============================

# Advance world time every Streamlit execution
clock.tick(minutes=15)

# Mother exists in world time
mother.tick()

# Gestation runs ONLY pre-birth
if not a7do.aware:
    gestation.tick()


# ==============================
# Observer Controls
# ==============================

st.sidebar.header("Observer Control")

if not a7do.aware:
    st.sidebar.info("A7DO is in pre-birth gestation.")
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()


# ==============================
# DISPLAY
# ==============================

st.title("SLED World – A7DO Cognitive Emergence")

# -------- World Time --------
st.subheader("World Time")
st.json(clock.snapshot())

# -------- Mother (World Agent) --------
st.subheader("Mother (World Agent)")
st.json(mother.snapshot(clock.world_datetime))

# -------- Gestation --------
st.subheader("Gestation Bridge")
st.json({
    "completed": gestation.completed,
    "elapsed_days": gestation.elapsed_days,
    "phase": gestation.phase,
})

# -------- A7DO --------
st.subheader("A7DO Subjective State")
st.json(a7do.snapshot())

# -------- A7DO Body --------
st.subheader("A7DO Body State (Observer Only)")
st.json(a7do.body.snapshot())

# -------- Familiarity --------
st.subheader("Pre-symbolic Familiarity Patterns")
st.json(a7do.familiarity.top())

# -------- Internal Log --------
st.subheader("Internal Log (Observer Only)")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log))
else:
    st.write("—")


# ==============================
# Footer
# ==============================

st.caption(
    "A7DO has no access to world time. "
    "All time, rhythm, and causality are mediated through gated sensory coupling."
)