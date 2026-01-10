import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_space import WEATHER_DEFAULTS
from world_core.world_clock import WorldClock  # if you already have this file; else use fallback below


# ---------------------------
# Fallback WorldClock (if you don't have world_core/world_clock.py)
# ---------------------------
try:
    WorldClock
except NameError:
    from datetime import datetime, timedelta

    class WorldClock:
        def __init__(self, acceleration: float = 1.0):
            self.acceleration = float(acceleration)
            self.world_datetime = datetime.utcnow()

        def tick(self, minutes: int = 1):
            self.world_datetime = self.world_datetime + timedelta(minutes=int(minutes))


st.set_page_config(page_title="SLEDWorld — Manager Dashboard", layout="wide")
st.title("SLEDWorld — Manager Dashboard")
st.caption("Reality → Sensors → Investigator → Ledger → Gates → (Manager approvals) → Higher layers")

# ==================================================
# Session init
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# ==================================================
# Top controls (ON PAGE, not sidebar)
# ==================================================
colA, colB, colC, colD = st.columns([1.2, 1.2, 1.2, 2.4])

with colA:
    advance_steps = st.number_input("Advance steps", min_value=1, max_value=200, value=10, step=1)

with colB:
    step_minutes = st.number_input("Minutes per step", min_value=1, max_value=60, value=1, step=1)

with colC:
    if st.button("▶ Advance World", use_container_width=True):
        for _ in range(int(advance_steps)):
            clock.tick(minutes=int(step_minutes))
            world.tick()

with colD:
    if st.button("Reset World (hard)", use_container_width=True):
        st.session_state.pop("world", None)
        st.session_state.pop("clock", None)
        st.rerun()

st.divider()

# ==================================================
# Manager approvals (manual holds)
# ==================================================
st.subheader("Manager Approvals (manual holds)")

m1, m2, m3, m4 = st.columns(4)

with m1:
    if st.button("Approve Neighbourhood Expansion", use_container_width=True):
        world.manager.manual_approve("neighbourhood")

with m2:
    if st.button("Approve People/Animals", use_container_width=True):
        world.manager.manual_approve("population")

with m3:
    if st.button("Approve Architect Layer", use_container_width=True):
        world.manager.manual_approve("architect")

with m4:
    if st.button("Approve Builder Layer", use_container_width=True):
        world.manager.manual_approve("builder")

st.caption("These approvals do not force learning; they only allow downstream layers to activate when gates are open.")

# ==================================================
# World + Gate summary
# ==================================================
st.divider()
st.subheader("World Summary")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Frame", world.frame)

with s2:
    st.metric("Places", len(world.places))

with s3:
    st.metric("Agents", len(world.agents))

with s4:
    st.metric("Ledger events", len(world.ledger.events))

st.subheader("Sandy’s Law Gates (live)")
g = world.ledger.gates_snapshot()

gc1, gc2, gc3, gc4 = st.columns(4)
gc1.metric("Object stability", f"{g['object_stability']:.3f}", "gate" if g["object_stable"] else "locked")
gc2.metric("Structure stability", f"{g['structure_stability']:.3f}", "gate" if g["structure_stable"] else "locked")
gc3.metric("Symbol readiness", f"{g['symbol_readiness']:.3f}", "gate" if g["symbol_ready"] else "locked")
gc4.metric("Language readiness", f"{g['language_readiness']:.3f}", "gate" if g["language_ready"] else "locked")

st.caption(
    f"Manual approvals: neighbourhood={world.manager.approved('neighbourhood')} · "
    f"population={world.manager.approved('population')} · "
    f"architect={world.manager.approved('architect')} · "
    f"builder={world.manager.approved('builder')}"
)

# ==================================================
# Render: aerial map + sensors
# ==================================================
st.divider()
st.subheader("Aerial Map (2D) + Sensors (Sound/Light)")

left, right = st.columns([1.0, 1.2])

with left:
    st.markdown("### World Aerial (occupancy)")
    occ = world.grid.render_occupancy(size=64)  # 0..1
    fig, ax = plt.subplots()
    ax.imshow(occ, interpolation="nearest")
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)

    st.markdown("### Surveyor surface (2.5D slice)")
    surf2d = world.surveyor.surface_slice_2d() if world.surveyor else None
    if surf2d is None:
        st.info("No surveyor configured.")
    else:
        fig, ax = plt.subplots()
        ax.imshow(surf2d, interpolation="nearest")
        ax.axis("off")
        st.pyplot(fig, use_container_width=True)

with right:
    st.markdown("### Scouts")
    sound = world.get_latest_sensor_grid("sound")
    light = world.get_latest_sensor_grid("light")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Sound field**")
        if sound is None:
            st.info("No sound scout yet.")
        else:
            fig, ax = plt.subplots()
            ax.imshow(sound, interpolation="nearest")
            ax.axis("off")
            st.pyplot(fig, use_container_width=True)

    with r2:
        st.markdown("**Light field**")
        if light is None:
            st.info("No light scout yet.")
        else:
            fig, ax = plt.subplots()
            ax.imshow(light, interpolation="nearest")
            ax.axis("off")
            st.pyplot(fig, use_container_width=True)

st.divider()

# ==================================================
# Bot snapshots (compact)
# ==================================================
st.subheader("Bots (compact snapshots)")

for a in world.agents:
    if hasattr(a, "snapshot"):
        snap = a.snapshot()
        with st.expander(f"{snap.get('source','agent')} · {snap.get('name', a.__class__.__name__)}", expanded=False):
            st.json(snap)

st.subheader("Scouts")
for s in world.scouts:
    snap = s.snapshot()
    with st.expander(f"{snap.get('source','scout')} · {snap.get('name','Scout')}", expanded=False):
        st.json({k: v for k, v in snap.items() if k != "grid"})  # don't dump huge grids

st.subheader("Ledger tail (last 20)")
tail = world.ledger.tail(20)
st.json(tail)

st.caption(
    "Manager page is the single place for advancing the world and approving new layers. "
    "Pages on the left show deeper views."
)