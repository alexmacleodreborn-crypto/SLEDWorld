import streamlit as st
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
# DEV / HARD RESET
# ==================================================
st.sidebar.header("Dev Controls")

if st.sidebar.button("🔄 HARD RESET WORLD"):
    st.session_state.clear()
    st.rerun()

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
    "Advance frames",
    min_value=1,
    max_value=50,
    value=5,
)

minutes_per_step = st.sidebar.slider(
    "Minutes per frame",
    min_value=1,
    max_value=60,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=minutes_per_step)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World (soft)"):
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
    "num_active_scouts": len(getattr(world, "scouts", [])),
})

# --------------------------
# Observer View
# --------------------------
st.subheader("Observer Perception")

observer_found = False
for agent in world.agents:
    if hasattr(agent, "observe") and hasattr(agent, "snapshot"):
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present in this world.")

# --------------------------
# Physical Agents (Walkers)
# --------------------------
st.subheader("Physical Agents")

for agent in world.agents:
    if hasattr(agent, "tick") and hasattr(agent, "snapshot") and not hasattr(agent, "observe"):
        st.json(agent.snapshot())

# --------------------------
# Active Scouts
# --------------------------
st.subheader("Active Scouts (Focused Attention)")

scouts = getattr(world, "scouts", [])

if scouts:
    for scout in scouts:
        st.json(scout.snapshot())
else:
    st.write("No active scouts.")

# --------------------------
# Scout Perception — Square View
# --------------------------
st.subheader("Scout Perception — Local Squares")

if not scouts:
    st.write("No active scouts to visualise.")
else:
    for scout in scouts:
        st.markdown(f"### {scout.name} — frame {scout.frame}")

        if not hasattr(scout, "sketches") or not scout.sketches:
            st.write("No sketches yet.")
            continue

        latest = scout.sketches[-1]

        colA, colB, colC = st.columns(3)

        with colA:
            st.caption("Occupancy (Shape / Outline)")
            st.image(
                np.array(latest["occupancy"]),
                clamp=True,
                use_column_width=True,
            )

        with colB:
            st.caption("Depth (Distance)")
            st.image(
                np.array(latest["depth"]),
                clamp=True,
                use_column_width=True,
            )

        with colC:
            st.caption("Sound Intensity")
            st.image(
                np.array(latest["sound"]),
                clamp=True,
                use_column_width=True,
            )

        # --------------------------
        # Shape persistence metric
        # --------------------------
        if hasattr(scout, "compute_persistence"):
            persistence = scout.compute_persistence()
            if persistence is not None:
                st.metric(
                    "Shape Persistence (IoU)",
                    f"{persistence:.3f}"
                )
            else:
                st.write("Shape persistence: insufficient frames")

# --------------------------
# Salience Investigator
# --------------------------
st.subheader("Salience Investigator (Accounting Layer)")

investigator = getattr(world, "salience_investigator", None)

if investigator is None:
    st.warning("Salience Investigator not present in this world instance.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.metric("Frames Processed", investigator.frame)
    st.metric("Ledger Entries", len(investigator.ledger))

with col2:
    st.json(investigator.snapshot())

# --------------------------
# Salience Ledger (Recent)
# --------------------------
st.subheader("Salience Ledger (Recent Entries)")

if investigator.ledger:
    st.json(investigator.ledger[-10:])
else:
    st.write("No salience records yet.")

# ==================================================
# Footer
# ==================================================
st.caption(
    "World exists independently · "
    "Walkers cause change · "
    "Observers perceive · "
    "Scouts focus attention · "
    "Shape precedes name · "
    "Time is a coordinate, not a driver"
)