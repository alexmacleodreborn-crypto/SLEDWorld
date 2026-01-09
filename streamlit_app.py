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
# Sidebar
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

# --------------------------
# Surveyors
# --------------------------
st.subheader("Surveyors — Physical Geometry")

if not world.surveyors:
    st.info("No active surveyors.")
else:
    for sv in world.surveyors:
        snap = sv.snapshot()
        with st.expander(f"{snap['name']} · frame {snap['frame']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("Occupancy (solid)")
                grid = np.array(snap["occupancy_grid"])
                fig, ax = plt.subplots()
                ax.imshow(grid, cmap="gray")
                ax.axis("off")
                st.pyplot(fig)

            with col2:
                st.write("Surface map")
                grid = np.array(snap["surface_grid"])
                fig, ax = plt.subplots()
                ax.imshow(grid, cmap="hot")
                ax.axis("off")
                st.pyplot(fig)

# --------------------------
# Investigator
# --------------------------
st.subheader("Salience Ledger")

investigator = world.salience_investigator
st.metric("Transactions", len(investigator.ledger))
st.json(investigator.ledger[-10:])

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Shape precedes meaning. "
    "Fields bind to surfaces. "
    "Time is optional."
)