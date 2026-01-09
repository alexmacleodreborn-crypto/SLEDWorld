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
# Session initialisation
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# ==================================================
# Sidebar – World Advancement
# ==================================================
st.sidebar.header("World Advancement")

steps = st.sidebar.slider("Advance frames", 1, 20, 1)

if st.sidebar.button("▶ Advance World"):
    for _ in range(steps):
        clock.tick(minutes=1)
        world.tick()

if st.sidebar.button("Reset World"):
    st.session_state.clear()
    st.rerun()

# ==================================================
# Main Display
# ==================================================
st.title("SLEDWorld – Reality Frame")

# ==================================================
# Surveyors — Geometry
# ==================================================
st.subheader("Surveyors — Physical Geometry")

surveyors = getattr(world, "surveyors", [])

if not surveyors:
    st.info("No active surveyors.")
else:
    for idx, sv in enumerate(surveyors):
        snap = sv.snapshot() or {}

        name = snap.get("name", f"Surveyor-{idx}")
        frame = snap.get("frame", "—")
        active = snap.get("active", False)

        with st.expander(f"{name} · frame {frame} · active={active}", expanded=False):

            occ = snap.get("occupancy_grid")
            surf = snap.get("surface_grid")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Occupancy (solid vs empty)**")
                if occ:
                    arr = np.array(occ)
                    fig, ax = plt.subplots()
                    ax.imshow(arr, cmap="gray")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No occupancy data yet.")

            with col2:
                st.markdown("**Surface map (edges)**")
                if surf:
                    arr = np.array(surf)
                    fig, ax = plt.subplots()
                    ax.imshow(arr, cmap="hot")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No surface data yet.")

# ==================================================
# Salience Investigator
# ==================================================
st.subheader("Salience Ledger")

investigator = getattr(world, "salience_investigator", None)

if investigator is None:
    st.warning("No salience investigator present.")
else:
    st.metric("Total Transactions", len(investigator.ledger))

    if investigator.ledger:
        st.subheader("Recent Transactions")
        st.json(investigator.ledger[-10:])
    else:
        st.write("No salience transactions yet.")

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Geometry precedes meaning. "
    "Fields bind to surfaces. "
    "Time is optional."
)