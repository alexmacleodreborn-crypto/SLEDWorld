import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

# ==================================================
# Streamlit config
# ==================================================
st.set_page_config(
    page_title="SLEDWorld – Reality Frame",
    layout="wide"
)

# ==================================================
# SESSION INITIALISATION (AUTHORITATIVE)
# ==================================================
# ⚠️ This block MUST be the only place build_world() is called

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# ==================================================
# SIDEBAR – WORLD ADVANCEMENT
# ==================================================
st.sidebar.header("World Advancement")

advance_steps = st.sidebar.slider(
    "Advance frames",
    min_value=1,
    max_value=50,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World (FULL RESET)"):
    st.session_state.clear()
    st.rerun()

# ==================================================
# MAIN DISPLAY
# ==================================================
st.title("SLEDWorld – Reality Frame")

# --------------------------
# WORLD FRAME COUNTER (PROOF OF PERSISTENCE)
# --------------------------
st.metric(
    "World Frame",
    getattr(world.space, "frame_counter", "N/A")
)

# --------------------------
# WORLD STATE
# --------------------------
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
    "num_surveyors": len(getattr(world, "surveyors", [])),
})

# --------------------------
# WORLD SPACE (GLOBAL FIELDS)
# --------------------------
st.subheader("🌍 World Space (Global Fields)")

if hasattr(world, "space"):
    st.json(world.space.snapshot())
else:
    st.warning("No world space present.")

# --------------------------
# AGENTS
# --------------------------
st.subheader("🤖 Agents")

for agent in world.agents:
    if hasattr(agent, "snapshot"):
        with st.expander(agent.name, expanded=False):
            st.json(agent.snapshot())

# --------------------------
# SCOUTS
# --------------------------
st.subheader("🕵 Scouts")

scouts = getattr(world, "scouts", [])
if not scouts:
    st.write("No active scouts.")
else:
    for scout in scouts:
        snap = scout.snapshot()
        with st.expander(scout.name, expanded=False):
            st.json(snap)

# --------------------------
# SURVEYORS — 3D GEOMETRY VIEW
# --------------------------
st.subheader("🧱 Surveyor Geometry")

surveyors = getattr(world, "surveyors", [])
if not surveyors:
    st.write("No surveyors active.")
else:
    for sv in surveyors:
        snap = sv.snapshot()
        with st.expander(sv.name, expanded=False):

            st.json({
                "frame": snap.get("frame"),
                "active": snap.get("active"),
                "center_xyz": snap.get("center_xyz"),
                "resolution_m": snap.get("resolution_m"),
                "volume_shape": snap.get("volume_shape"),
            })

            vol = snap.get("volume")
            surf = snap.get("surface_volume")

            if vol and surf:
                nz = len(vol)

                z_slice = st.slider(
                    f"Z layer – {sv.name}",
                    min_value=0,
                    max_value=nz - 1,
                    value=0,
                    key=f"{sv.name}_z"
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

# --------------------------
# SALIENCE INVESTIGATOR
# --------------------------
st.subheader("🧠 Salience Investigator")

investigator = getattr(world, "salience_investigator", None)

if investigator:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Frames Processed", investigator.frame_counter)
        st.metric("Ledger Entries", len(investigator.ledger))

    with col2:
        st.json(investigator.snapshot())

    if investigator.ledger:
        st.subheader("Recent Ledger (last 10)")
        st.json(investigator.ledger[-10:])
else:
    st.warning("No salience investigator present.")

# ==================================================
# FOOTER
# ==================================================
st.caption(
    "Reality persists independently. "
    "Agents act. "
    "Observers perceive. "
    "Structure emerges before meaning."
)