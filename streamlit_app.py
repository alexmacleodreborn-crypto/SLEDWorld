import streamlit as st

# -------------------------------
# Imports (current architecture)
# -------------------------------
from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

from world_core.world_state import WorldState
from world_core.world_clock import WorldClock
from world_core.world_bootstrap import bootstrap_world
from world_core.intersection_gate import perceived_snapshot

from experience_layer.sensory_drip import sensory_drip


# -------------------------------
# Streamlit config
# -------------------------------
st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide"
)

st.title("🧠 SLED World – A7DO Cognitive Emergence")


# -------------------------------
# Session State Bootstrap
# -------------------------------
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "world" not in st.session_state:
    st.session_state.world = bootstrap_world()

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(
        a7do=st.session_state.a7do,
        world=st.session_state.world,
        clock=st.session_state.clock
    )


a7do = st.session_state.a7do
world = st.session_state.world
clock = st.session_state.clock
cycle = st.session_state.cycle


# -------------------------------
# WORLD STATUS
# -------------------------------
with st.sidebar:
    st.header("🌍 World Status")

    st.write(f"**World Time (days):** {clock.day}")
    st.write(f"**World Hour:** {clock.hour:02d}:00")
    st.write(f"**A7DO Awake:** {a7do.is_awake}")
    st.write(f"**A7DO Birthed:** {a7do.birthed}")

    st.divider()

    st.subheader("A7DO Body State")
    st.json(a7do.body.snapshot())

    st.subheader("Familiarity (top patterns)")
    st.write(a7do.familiarity.top(5))


# -------------------------------
# BIRTH CONTROL
# -------------------------------
st.header("🍼 Birth & Development Control")

if not a7do.birthed:
    st.info("A7DO is in pre-birth state (gated perception).")

    if st.button("Begin Birth Transition"):
        cycle.ensure_birth()
        st.success("Birth transition initiated.")
        st.experimental_rerun()


# -------------------------------
# AWAKE EXPERIENCE LOOP
# -------------------------------
if a7do.birthed and a7do.is_awake:
    st.header("👁️ Live Experience (Awake)")

    # World advances one tick
    clock.tick()
    world.tick(clock)

    # Perceived snapshot (intersection gate)
    snapshot = perceived_snapshot(world, a7do)

    # Sensory drip derived ONLY from snapshot
    drip = sensory_drip(snapshot)

    # Apply perception to A7DO
    a7do.apply_sensory(drip)

    st.subheader("Perceived Snapshot")
    st.json(snapshot)

    st.subheader("Sensory Drip Applied")
    st.json(drip)

    if st.button("Induce Sleep"):
        cycle.sleep()
        st.experimental_rerun()


# -------------------------------
# SLEEP PHASE
# -------------------------------
if a7do.birthed and not a7do.is_awake:
    st.header("🌙 Sleep Phase")

    replayed = a7do.sleep()

    st.subheader("Replay / Consolidation")
    st.write(replayed)

    if st.button("Wake for Next Day"):
        cycle.wake()
        st.experimental_rerun()


# -------------------------------
# INTERNAL LOG
# -------------------------------
st.header("📜 Internal Log")

for line in a7do.internal_log[-20:]:
    st.write(line)


# -------------------------------
# FOOTER
# -------------------------------
st.divider()
st.caption(
    "SLED World – Developmental cognition via gated perception, "
    "continuous world time, and embodied learning."
)