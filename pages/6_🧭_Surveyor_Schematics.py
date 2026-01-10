# pages/6_🧭_Surveyor_Schematics.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🧭 Surveyor Schematics (Occupancy / Surface)")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

# Find surveyor snapshot
surveyor_snap = None
for a in getattr(world, "agents", []):
    if getattr(a, "__class__", None) and a.__class__.__name__ == "SurveyorBot":
        surveyor_snap = a.snapshot()
        break

if not surveyor_snap or "volume" not in surveyor_snap:
    st.warning("No SurveyorBot volume found. Add SurveyorBot to bootstrap if needed.")
    st.stop()

vol = np.array(surveyor_snap["volume"])
surf = np.array(surveyor_snap.get("surface_volume", vol * 0))

st.subheader("Slice controls")
z = st.slider("Z slice", 0, vol.shape[0] - 1, 0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Solid occupancy (1/0)")
    fig, ax = plt.subplots()
    ax.imshow(vol[z], interpolation="nearest")
    ax.axis("off")
    st.pyplot(fig)

with col2:
    st.subheader("Surface voxels")
    fig, ax = plt.subplots()
    ax.imshow(surf[z], interpolation="nearest")
    ax.axis("off")
    st.pyplot(fig)

st.caption("This is your schematic substrate. Architect/Builder read patterns from here.")