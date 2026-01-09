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

advance_steps = st.sidebar.slider(
    "Advance steps",
    min_value=1,
    max_value=20,
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

# --------------------------
# World State
# --------------------------
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------
# World Geometry & Objects
# --------------------------
st.subheader("World Geometry & Objects")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json({
            "position": getattr(place, "position", None),
            "bounds": getattr(place, "bounds", None),
        })

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                with st.expander(f"Room: {room.name}", expanded=False):
                    room_view = {
                        "bounds": getattr(room, "bounds", None),
                        "objects": {},
                    }

                    if hasattr(room, "objects"):
                        for obj_name, obj in room.objects.items():
                            if hasattr(obj, "snapshot"):
                                room_view["objects"][obj_name] = obj.snapshot()
                            else:
                                room_view["objects"][obj_name] = str(obj)

                    st.json(room_view)

# --------------------------
# Observer Perception
# --------------------------
st.subheader("Observer Perception")

observer_found = False
for agent in world.agents:
    if agent.__class__.__name__ == "ObserverBot":
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present.")

# --------------------------
# World Agents
# --------------------------
st.subheader("World Agents")

for agent in world.agents:
    if hasattr(agent, "snapshot"):
        st.json(agent.snapshot())

# --------------------------
# Salience Investigator
# --------------------------
st.subheader("Salience Ledger (Accounting)")

investigator = getattr(world, "salience_investigator", None)

if investigator:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Frames Processed", investigator.frame_counter)
        st.metric("Total Transactions", len(investigator.ledger))

    with col2:
        st.json(investigator.snapshot())

    st.subheader("Recent Salience Transactions")
    st.json(investigator.ledger[-10:])
else:
    st.warning("No salience investigator present.")

# ==================================================
# Scout Visual Perception (NEW – THIS IS THE KEY PART)
# ==================================================
st.divider()
st.subheader("Scout Perception — Shape & Sound")

scouts = getattr(world, "scouts", [])

if not scouts:
    st.write("No active scouts.")
else:
    for scout in scouts:
        snap = scout.snapshot()

        st.markdown(f"### {scout.name}")
        st.caption(
            f"Frame {snap['frame']} · "
            f"Active: {snap['active']} · "
            f"Persistence: {snap['shape_persistence']}"
        )

        colA, colB, colC = st.columns(3)

        # ------------------
        # Shape (Occupancy)
        # ------------------
        with colA:
            st.markdown("**Shape (Occupancy)**")
            fig, ax = plt.subplots()
            ax.imshow(
                scout.occupancy,
                cmap="gray",
                origin="lower"
            )
            ax.set_title("Occupied Space")
            ax.axis("off")
            st.pyplot(fig)

        # ------------------
        # Sound Field
        # ------------------
        with colB:
            st.markdown("**Sound Field**")
            fig, ax = plt.subplots()
            ax.imshow(
                scout.sound,
                cmap="inferno",
                origin="lower"
            )
            ax.set_title("Sound Intensity")
            ax.axis("off")
            st.pyplot(fig)

        # ------------------
        # Metrics
        # ------------------
        with colC:
            st.metric("Shape Persistence", snap["shape_persistence"])
            st.metric("Occupied Cells", snap["occupancy_sum"])
            st.metric("Sound Energy", snap["sound_sum"])

        st.divider()

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Structure precedes meaning. "
    "Change binds to shape. "
    "Understanding emerges."
)