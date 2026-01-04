import streamlit as st
import time

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge

from world_core.world_clock import WorldClock
from world_core.mother_bot import MotherBot
from world_core.heartbeat_field import HeartbeatField  # ✅ correct location

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

# -------------------------
# Session init
# -------------------------
if "clock" not in st.session_state:
    # 1 real second can represent accelerated world seconds in WorldClock
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

# Optional: keep an observer-visible “world heart” (not required, but useful)
if "world_heartbeat" not in st.session_state:
    st.session_state.world_heartbeat = HeartbeatField(bpm=72.0)

clock: WorldClock = st.session_state.clock
a7do: A7DOState = st.session_state.a7do
mother: MotherBot = st.session_state.mother
gestation: GestationBridge = st.session_state.gestation
cycle: DayCycle = st.session_state.cycle
world_hb: HeartbeatField = st.session_state.world_heartbeat


# -------------------------
# Observer controls
# -------------------------
st.sidebar.header("Observer Control")

# Time step controls (so you can speed/slow without breaking logic)
minutes_step = st.sidebar.slider("World minutes per tick", 1, 60, 15, 1)
auto_tick = st.sidebar.toggle("Auto tick", value=True)

colA, colB = st.sidebar.columns(2)
with colA:
    do_tick = st.button("Tick once")
with colB:
    do_10 = st.button("Tick x10")

st.sidebar.divider()

if not a7do.aware:
    st.sidebar.info("A7DO is in pre-birth gestation (womb coupling).")
else:
    if st.sidebar.button("Wake A7DO"):
        cycle.wake()

    if st.sidebar.button("Sleep A7DO"):
        cycle.sleep()
        cycle.next_day()

st.sidebar.divider()
show_debug = st.sidebar.toggle("Show debug", value=True)


# -------------------------
# WORLD TICK LOOP
# -------------------------
def tick_once(step_minutes: int):
    # Advance world time
    clock.tick(minutes=step_minutes)

    # Advance world background heart rhythm (optional)
    world_hb.tick_minutes(step_minutes)

    # Mother exists in world time
    mother.tick()

    # If A7DO not aware yet, gestation coupling runs automatically
    if not a7do.aware:
        gestation.tick()


if do_tick:
    tick_once(minutes_step)

if do_10:
    for _ in range(10):
        tick_once(minutes_step)

# If you want it to move without buttons:
# Streamlit can’t truly “run a background loop” reliably without reruns.
# We implement a safe auto-tick by updating once per render and letting UI rerun.
if auto_tick:
    tick_once(minutes_step)


# -------------------------
# UI
# -------------------------
st.title("SLED World – A7DO Cognitive Emergence")

c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("World Time")
    st.json(clock.snapshot())

    st.subheader("World Heartbeat (background)")
    st.json(world_hb.snapshot())

    st.subheader("Mother (World Agent)")
    # mother.snapshot expects a datetime per your earlier usage
    try:
        st.json(mother.snapshot(clock.world_datetime))
    except TypeError:
        # if your mother.snapshot takes no args
        st.json(mother.snapshot())

    st.subheader("Gestation Bridge")
    # show defensively in case your bridge uses different property names
    gb = {
        "completed": getattr(gestation, "completed", None),
        "elapsed_days": getattr(gestation, "elapsed_days", None),
        "phase": getattr(gestation, "phase", None),
    }
    st.json(gb)

with c2:
    st.subheader("A7DO Subjective State")
    st.json(a7do.snapshot() if hasattr(a7do, "snapshot") else {"aware": getattr(a7do, "aware", None)})

    st.subheader("A7DO Body State (Observer Only)")
    if hasattr(a7do, "body") and hasattr(a7do.body, "snapshot"):
        st.json(a7do.body.snapshot())
    else:
        st.write("Body state not available.")

    st.subheader("Pre-symbolic Familiarity Patterns")
    if hasattr(a7do, "familiarity") and hasattr(a7do.familiarity, "top"):
        st.json(a7do.familiarity.top())
    else:
        st.write("Familiarity tracker not available.")

    st.subheader("Internal Log (Observer Only)")
    log = getattr(a7do, "internal_log", None)
    if log:
        st.code("\n".join(log))
    else:
        st.write("—")

if show_debug:
    st.divider()
    st.subheader("Debug")
    st.write("A7DO aware:", getattr(a7do, "aware", None))
    st.write("A7DO phase:", getattr(a7do, "phase", None))
    st.write("Minutes step:", minutes_step)
    st.write("Auto tick:", auto_tick)

st.caption(
    "A7DO has no access to world time. All causality emerges through gated sensory coupling."
)