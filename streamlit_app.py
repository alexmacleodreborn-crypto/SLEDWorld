import time
import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot

# =========================================================
# Streamlit setup
# =========================================================

st.set_page_config(
    page_title="SLED World — Observer",
    layout="wide"
)

# =========================================================
# Session state initialisation
# =========================================================

if "last_real_tick" not in st.session_state:
    st.session_state.last_real_tick = time.time()

if "world_clock" not in st.session_state:
    st.session_state.world_clock = WorldClock(acceleration=1000.0)

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
        clock=st.session_state.world_clock,
    )

clock = st.session_state.world_clock
mother = st.session_state.mother
a7do = st.session_state.a7do
gestation = st.session_state.gestation

# =========================================================
# WORLD TICK LOOP (authoritative time)
# =========================================================

now = time.time()
delta = now - st.session_state.last_real_tick

# Advance world every real second
if delta >= 1.0:
    st.session_state.last_real_tick = now

    # Advance world time
    clock.tick(real_seconds=delta)

    # Advance gestation & prebirth experience
    gestation.tick()

    # Force Streamlit refresh
    st.experimental_rerun()

# =========================================================
# OBSERVER DISPLAY
# =========================================================

st.title("🧭 SLED World — Observer View")

st.markdown(
    """
This panel shows **objective world reality**.  
A7DO does **not** have access to this information.
"""
)

# ---------------------------------------------------------
# World Time (objective)
# ---------------------------------------------------------

st.subheader("🌍 World Time (Objective)")

st.json({
    "datetime": clock.world_datetime.isoformat(),
    "day_index": clock.world_day_index,
    "time_of_day": clock.world_time_of_day,
    "acceleration": clock.acceleration,
})

# ---------------------------------------------------------
# Gestation state
# ---------------------------------------------------------

st.subheader("🤰 Gestation")

st.json({
    "phase": gestation.phase,
    "completed": gestation.completed,
    "elapsed_days": round(clock.world_day_index + clock.world_time.hour / 24, 3),
})

# ---------------------------------------------------------
# Mother (world entity)
# ---------------------------------------------------------

st.subheader("👩 Mother (World Entity)")

st.json(mother.snapshot(clock.world_datetime))

# ---------------------------------------------------------
# A7DO Internal State (no time)
# ---------------------------------------------------------

st.subheader("👶 A7DO Internal State")

st.json({
    "phase": a7do.phase,
    "aware": a7do.aware,
    "heartbeat_bpm": a7do.body.heartbeat.bpm,
})

# ---------------------------------------------------------
# Familiarity (pre-symbolic)
# ---------------------------------------------------------

st.subheader("🧠 Familiarity Patterns (Pre-Symbolic)")

st.json(a7do.familiarity.top())

# ---------------------------------------------------------
# Internal log (observer-visible only)
# ---------------------------------------------------------

st.subheader("📜 Internal Log")

st.code(
    "\n".join(a7do.internal_log[-25:])
    if a7do.internal_log
    else "—"
)