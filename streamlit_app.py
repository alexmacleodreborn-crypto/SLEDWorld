import streamlit as st

# =========================
# Core imports
# =========================

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot


# =========================
# Streamlit config
# =========================

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)


# =========================
# Session initialisation
# =========================

# --- WORLD CLOCK (absolute, real-time driven) ---
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=60.0)  # 1 real sec = 1 world min

# --- A7DO (subjective entity, no time awareness) ---
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

# --- Mother (world agent, lives in world time) ---
if "mother" not in st.session_state:
    st.session_state.mother = MotherBot(st.session_state.clock)

# --- Gestation bridge (world → a7do coupling) ---
if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
        clock=st.session_state.clock,
    )

# --- Post-birth day cycle (sleep / wake only after awareness) ---
if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)


# =========================
# Local handles
# =========================

clock = st.session_state.clock
a7do = st.session_state.a7do
mother = st.session_state.mother
gestation = st.session_state.gestation
cycle = st.session_state.cycle


# =========================
# WORLD TICK (ALWAYS RUNS)
# =========================
# This is the heart of everything.
# No buttons. No shortcuts. No manual stepping.

clock.tick()                 # advances world time based on real elapsed time
mother.tick()                # heartbeat, physiology, routine (world-time driven)

# Pre-birth coupling runs automatically until awareness unlocks
if not a7do.aware:
    gestation.tick()


# =========================
# Observer controls
# =========================

st.sidebar.header("Observer Control")

if not a7do.aware:
    st.sidebar.info("A7DO is in pre-birth gestation.\nWorld runs continuously.")
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()


# =========================
# DISPLAY (Observer-only)
# =========================

st.title("SLED World – A7DO Cognitive Emergence")

# --- World time ---
st.subheader("World Time")
st.json(clock.snapshot())

# --- Mother (world agent) ---
st.subheader("Mother (World Agent)")
st.json(mother.snapshot(clock.world_datetime))

# --- Gestation bridge ---
st.subheader("Gestation Bridge")
st.json({
    "completed": gestation.completed,
    "elapsed_days": gestation.elapsed_days,
    "phase": gestation.phase,
})

# --- A7DO subjective state ---
st.subheader("A7DO Subjective State")
st.json(a7do.snapshot())

# --- A7DO body (observer only) ---
st.subheader("A7DO Body State (Observer Only)")
st.json(a7do.body.snapshot())

# --- Pre-symbolic familiarity ---
st.subheader("Pre-symbolic Familiarity Patterns")
st.json(a7do.familiarity.top())

# --- Internal log ---
st.subheader("Internal Log (Observer Only)")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log))
else:
    st.write("—")

st.caption(
    "A7DO has no access to world time. "
    "Causality emerges only through gated sensory coupling."
)