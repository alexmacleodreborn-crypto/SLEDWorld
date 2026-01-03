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

# -------------------------------------------------
# Session initialisation (runs once)
# -------------------------------------------------

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()
    st.session_state.clock.start()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "mother" not in st.session_state:
    st.session_state.mother = MotherBot()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge(
        a7do=st.session_state.a7do,
        mother=st.session_state.mother,
        clock=st.session_state.clock,
    )

# -------------------------------------------------
# Aliases
# -------------------------------------------------

clock = st.session_state.clock
a7do = st.session_state.a7do
mother = st.session_state.mother
cycle = st.session_state.cycle
gestation = st.session_state.gestation

# -------------------------------------------------
# WORLD TIME TICK (ALWAYS RUNS)
# -------------------------------------------------

# 15 minutes of world time per UI refresh
clock.tick(minutes=15)

# -------------------------------------------------
# PRE-BIRTH / GESTATION COUPLING
# -------------------------------------------------

if not gestation.completed:
    gestation.tick()

# -------------------------------------------------
# UI — Observer View (READ ONLY)
# -------------------------------------------------

st.title("🧠 SLED World – A7DO Cognitive Emergence")

st.subheader("🌍 World Time")
st.json(clock.snapshot())

st.subheader("👶 A7DO State")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)

st.subheader("🤰 Gestation")
st.write("Completed:", gestation.completed)
st.write("Elapsed days:", round(gestation.elapsed_days, 2))

st.subheader("❤️ Mother Physiology")
st.json(mother.snapshot())

st.subheader("🧠 Familiarity (Pre-symbolic Patterns)")
st.json(a7do.familiarity.top())

st.subheader("📜 Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")

# -------------------------------------------------
# POST-BIRTH CONTROLS (appear only after birth)
# -------------------------------------------------

if gestation.completed and not a7do.birthed:
    st.success("Gestation complete — birth imminent")
    if st.button("Trigger Birth"):
        cycle.ensure_birth()

if a7do.birthed:
    st.sidebar.header("Observer Control")

    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()