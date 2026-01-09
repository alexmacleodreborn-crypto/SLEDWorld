import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")

# --------------------
# Session init
# --------------------
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# --------------------
# Sidebar controls
# --------------------
st.sidebar.header("World Control")

steps = st.sidebar.slider("Advance frames", 1, 50, 1)

if st.sidebar.button("▶ Advance World"):
    for _ in range(steps):
        clock.tick(minutes=1)
        world.tick()

if st.sidebar.button("Reset World"):
    st.session_state.clear()
    st.rerun()

# --------------------
# Main
# --------------------
st.title("SLEDWorld — Reality Frame")

# --------------------
# WorldSpace
# --------------------
st.subheader("🌍 World Space (Global Fields)")
ws = world.space.snapshot()
st.json(ws)

# --------------------
# Agents overview
# --------------------
st.subheader("🤖 Agents")
for a in world.agents:
    if hasattr(a, "snapshot"):
        st.json(a.snapshot())

# --------------------
# Scouts
# --------------------
st.subheader("🕵 Scouts")
for sc in world.scouts:
    snap = sc.snapshot()
    with st.expander(sc.name):
        st.json(snap)

# --------------------
# Surveyors — 3D VOLUME VIEW
# --------------------
st.subheader("🧱 Surveyor — 3D World Volume")

for sv in world.surveyors:
    snap = sv.snapshot()
    with st.expander(sv.name):
        st.json({
            "frame": snap.get("frame"),
            "active": snap.get("active"),
            "volume_shape": snap.get("volume_shape"),
        })

        vol = snap.get("volume")
        surf = snap.get("surface_volume")

        if vol and surf:
            nz = len(vol)
            z_slice = st.slider(
                f"Z layer ({sv.name})",
                min_value=0,
                max_value=nz - 1,
                value=0,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("Solid volume (XY slice)")
                arr = np.array(vol[z_slice])
                fig, ax = plt.subplots()
                ax.imshow(arr, cmap="gray")
                ax.set_title(f"Z = {z_slice}")
                ax.axis("off")
                st.pyplot(fig)

            with col2:
                st.write("Surface edges (XY slice)")
                arr = np.array(surf[z_slice])
                fig, ax = plt.subplots()
                ax.imshow(arr, cmap="hot")
                ax.set_title(f"Z = {z_slice}")
                ax.axis("off")
                st.pyplot(fig)
        else:
            st.warning("No volume data yet.")

# --------------------
# Investigator
# --------------------
st.subheader("🧠 Salience Investigator")
inv = world.salience_investigator
st.json(inv.snapshot())

if inv.ledger:
    st.subheader("Recent Ledger")
    st.json(inv.ledger[-10:])

# --------------------
# Footer
# --------------------
st.caption(
    "Reality persists • Structure emerges • Meaning follows evidence"
)