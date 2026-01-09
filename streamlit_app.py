import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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

advance_steps = st.sidebar.slider(
    "Advance steps (minutes per click)",
    min_value=1,
    max_value=25,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

# ==================================================
# Main Display
# ==================================================
st.title("SLEDWorld – Reality Frame")

# --------------------------------------------------
# World State
# --------------------------------------------------
st.subheader("World State")

st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------------------------------
# World Geometry & Objects
# --------------------------------------------------
st.subheader("World Geometry & Objects")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json(place.snapshot())

# --------------------------------------------------
# Observer Perception
# --------------------------------------------------
st.subheader("Observer Perception (Raw Fields)")

observer_found = False
for agent in world.agents:
    if agent.__class__.__name__ == "ObserverBot":
        observer_found = True
        snap = agent.snapshot()

        st.metric("Frames Observed", snap.get("frames_observed", 0))

        for room in snap.get("rooms", []):
            st.json(room)

if not observer_found:
    st.warning("No observer present.")

# --------------------------
# Salience Investigator
# --------------------------
st.subheader("Salience Ledger (Accounting)")

investigator = getattr(world, "salience_investigator", None)

if investigator:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Frames", investigator.frame_counter)
        st.metric("Events Logged", len(investigator.ledger))

    with col2:
        st.json(investigator.snapshot())

    st.subheader("Recent Events (Field Deltas)")
    if investigator.ledger:
        st.json(investigator.ledger[-12:])
    else:
        st.write("No events detected yet.")
else:
    st.warning("No salience investigator present.")
# --------------------------------------------------
# Scout Perception (LEDGER-DERIVED)
# --------------------------------------------------
st.divider()
st.subheader("Scout Perception — Confirmed Structure")

scouts = getattr(world, "scouts", [])

if not scouts:
    st.write("No active scouts.")
else:
    for scout in scouts:
        snap = scout.snapshot()

        st.markdown(f"### {scout.name}")
        st.caption(
            f"Frame {snap['frame']} · "
            f"Confirmed rooms {len(snap.get('confirmed_rooms', []))} · "
            f"Active {snap['active']}"
        )

        # Diagnostics
        with st.expander("Certainty Diagnostics", expanded=False):
            st.write("Rooms seen (certainty counts):")
            st.json(snap.get("rooms_seen", {}))

        col1, col2, col3 = st.columns(3)

        # ----------------------
        # Shape (CERTAIN)
        # ----------------------
        with col1:
            st.markdown("**Shape (Confirmed Existence)**")
            fig, ax = plt.subplots()
            ax.imshow(scout.shape, cmap="gray", origin="lower")
            ax.axis("off")
            st.pyplot(fig)

        # ----------------------
        # Sound (CERTAIN)
        # ----------------------
        with col2:
            st.markdown("**Sound Signature**")
            fig, ax = plt.subplots()
            ax.imshow(scout.sound, cmap="inferno", origin="lower")
            ax.axis("off")
            st.pyplot(fig)

        # ----------------------
        # Light (CERTAIN)
        # ----------------------
        with col3:
            st.markdown("**Light Signature**")
            fig, ax = plt.subplots()
            ax.imshow(scout.light, cmap="plasma", origin="lower")
            ax.axis("off")
            st.pyplot(fig)

        st.divider()

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Observers report raw fields. "
    "Salience integrates certainty. "
    "Scouts visualise confirmed structure. "
    "Meaning is not assumed."
)