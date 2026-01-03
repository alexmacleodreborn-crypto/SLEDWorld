# sledworld/streamlit_app.py

import streamlit as st
import sys
import os

# --------------------------------------------------
# Ensure local packages resolve correctly
# --------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# --------------------------------------------------
# Core imports (aligned with your structure)
# --------------------------------------------------

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot

# --------------------------------------------------
# Streamlit config
# --------------------------------------------------

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

st.title("🧠 SLED World — A7DO Cognitive Emergence")

# --------------------------------------------------
# Session state initialisation
# --------------------------------------------------

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
    )

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

clock = st.session_state.clock
mother = st.session_state.mother
a7do = st.session_state.a7do
gestation = st.session_state.gestation
cycle = st.session_state.cycle

# --------------------------------------------------
# World time tick (ALWAYS RUNS)
# --------------------------------------------------

# Each UI refresh advances world time
# 15 minutes of world time per refresh
clock.tick(minutes=15)

DT_SECONDS = 1.0  # physiological timestep

# --------------------------------------------------
# Pre-birth gestation (automatic, no buttons)
# --------------------------------------------------

if not gestation.completed:
    gestation.tick(
        dt_seconds=DT_SECONDS,
        world_days_elapsed=clock.days_elapsed,
    )

# --------------------------------------------------
# Post-birth cycle handling
# --------------------------------------------------

if gestation.completed and not cycle.has_birthed:
    cycle.ensure_birth()

# --------------------------------------------------
# Observer controls (minimal by design)
# --------------------------------------------------

st.sidebar.header("Observer Controls")

if a7do.birthed:
    if not a7do.is_awake:
        if st.sidebar.button("Wake"):
            cycle.wake()
    else:
        if st.sidebar.button("Sleep"):
            cycle.sleep()
            cycle.next_day()

# --------------------------------------------------
# Display panels
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 World Time")
    st.json({
        "days_elapsed": round(clock.days_elapsed, 2),
        "time_of_day": clock.time_of_day,
        "running": clock.running,
    })

    st.subheader("🤰 Mother (External)")
    st.json(mother.snapshot())

with col2:
    st.subheader("👶 A7DO State")
    st.write("Birthed:", a7do.birthed)
    st.write("Awake:", a7do.is_awake)

    st.subheader("❤️ A7DO Body")
    st.json(a7do.body.snapshot())

# --------------------------------------------------
# Internal cognitive traces (observer-visible)
# --------------------------------------------------

st.subheader("🧩 Familiarity Patterns (Pre-Symbolic)")
st.json(a7do.familiarity.top())

st.subheader("🧠 Internal Log")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log))
else:
    st.write("—")

# --------------------------------------------------
# Auto-refresh (keeps time moving)
# --------------------------------------------------

st.caption("World is running continuously. UI refresh drives time.")