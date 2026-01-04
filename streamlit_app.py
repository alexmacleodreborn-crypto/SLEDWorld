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
    # Accelerated world time: 1 real sec = 60 world sec
    st.session_state.clock = WorldClock(acceleration=60)

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
# WORLD TICK (authoritative)
# =========================

def tick_once(step_minutes: int):
    # Advance world time
    clock.tick(minutes=step_minutes)

    # Mother exists in world time
    mother.tick()

    # Gestation runs automatically until awareness unlock
    if not a7do.aware:
        gestation.tick()


# =========================
# Observer Controls
# =========================

st.sidebar.header("Observer Control")

minutes_step = st.sidebar.slider(
    "World minutes per tick",
    min_value=1,
    max_value=60,
    value=15,
    step=1,
)

auto_tick = st.sidebar.toggle("Auto tick", value=True)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Tick once"):
        tick_once(minutes_step)
with col2:
    if st.button("Tick x10"):
        for _ in range(10):
            tick_once(minutes_step)

st.sidebar.divider()

if not a7do.aware:
    st.sidebar.info("A7DO is in pre-birth gestation.")
else:
    if st.sidebar.button("Wake A7DO"):
        cycle.wake()

    if st.sidebar.button("Sleep A7DO"):
        cycle.sleep()
        cycle.next_day()


# Auto progression (safe)
if auto_tick:
    tick_once(minutes_step)


# =========================
# DISPLAY
# =========================

st.title("SLED World – A7DO Cognitive Emergence")

c1, c2 = st.columns(2)

with c1:
    st.subheader("World Time")
    st.json(clock.snapshot())

    st.subheader("Mother (World Agent)")
    try:
        st.json(mother.snapshot(clock.world_datetime))
    except TypeError:
        st.json(mother.snapshot())

    st.subheader("Gestation Bridge")
    st.json({
        "completed": getattr(gestation, "completed", None),
        "elapsed_days": getattr(gestation, "elapsed_days", None),
        "phase": getattr(gestation, "phase", None),
    })

with c2:
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