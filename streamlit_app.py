import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot


st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

# =========================
# Session initialisation
# =========================

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=60)  # 1 sec = 60 world sec

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


clock = st.session_state.clock
a7do = st.session_state.a7do
mother = st.session_state.mother
gestation = st.session_state.gestation
cycle = st.session_state.cycle


# =========================
# WORLD TICK (always runs)
# =========================

# Advance world time by 15 minutes per UI refresh
clock.tick(minutes=15)

# Mother lives in world time
mother.tick()

# Pre-birth gestation runs automatically
if not a7do.aware:
    gestation.tick()


# =========================
# Observer Controls
# =========================

st.sidebar.header("Observer Control")

if not a7do.aware:
    st.sidebar.info("A7DO is in pre-birth gestation.")
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()


# =========================
# DISPLAY
# =========================

st.title("SLED World – A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("Mother (World Agent)")
st.json(mother.snapshot(clock.world_datetime))

st.subheader("Gestation Bridge")
st.json({
    "completed": gestation.completed,
    "elapsed_days": gestation.elapsed_days,
    "phase": gestation.phase,
})

st.subheader("A7DO Subjective State")
st.json(a7do.snapshot())

st.subheader("A7DO Body State (Observer Only)")
st.json(a7do.body.snapshot())

st.subheader("Pre-symbolic Familiarity Patterns")
st.json(a7do.familiarity.top())

st.subheader("Internal Log (Observer Only)")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log))
else:
    st.write("—")

st.caption(
    "A7DO has no access to world time. "
    "All causality emerges through gated sensory coupling."
)