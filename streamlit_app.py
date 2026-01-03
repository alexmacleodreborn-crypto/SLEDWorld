import time
import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# =========================
# Session initialisation
# =========================

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()

if "gestation" not in st.session_state:
    st.session_state.gestation = GestationBridge()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()

a7do = st.session_state.a7do
clock = st.session_state.clock
gestation = st.session_state.gestation
cycle = st.session_state.cycle

# =========================
# TIME BOT (critical)
# =========================

now = time.time()
elapsed = now - st.session_state.last_tick

# 1 second real = 15 minutes world
WORLD_MINUTES_PER_SECOND = 15

if elapsed >= 1.0:
    clock.seconds_elapsed += elapsed * WORLD_MINUTES_PER_SECOND * 60
    st.session_state.last_tick = now

    # gestation always advances
    gestation.tick(clock)

    # pre-birth sensory substrate
    if not a7do.birthed:
        a7do.familiarity.observe(
            place="womb",
            channels={
                "heartbeat": 0.6,
                "pressure": 0.3,
                "muffled_sound": 0.25,
            },
            intensity=0.2,
        )

    # auto birth trigger
    if not a7do.birthed and gestation.ready_for_birth():
        cycle.ensure_birth()
        gestation.mark_completed()
        a7do.internal_log.append("transition: womb → birth")

    # force next tick
    st.experimental_rerun()

# =========================
# Observer controls
# =========================

st.sidebar.header("Observer")

if a7do.birthed:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

# =========================
# Display
# =========================

st.title("SLED World – A7DO Cognitive Emergence")

st.subheader("World Time")
st.json(clock.snapshot())

st.subheader("Gestation")
st.write("Elapsed days:", round(gestation.elapsed_days, 2))
st.write("Completed:", gestation.completed)

st.subheader("A7DO State")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perceived place:", a7do.perceived_place)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log[-20:]) if a7do.internal_log else "—")

st.subheader("Familiarity (top patterns)")
st.json(a7do.familiarity.top())

st.caption("⏱ Time bot active: 1s real = 15min world")