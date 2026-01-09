# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock


st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")
st.title("SLEDWorld – Reality Frame")
st.caption("Reality → Perception → Ledger → Scouts (shape/sound/light)")

# Session init
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# Sidebar controls
st.sidebar.header("World Advancement")
advance_steps = st.sidebar.slider("Advance steps", 1, 50, 5)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()
if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

# Main: World state
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
})

# Geometry & objects
st.subheader("World Geometry & Objects")
for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json({
            "position": getattr(place, "position", None),
            "bounds": getattr(place, "bounds", None),
        })

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                rs = room.snapshot()
                with st.expander(f"Room: {room.name} ({rs.get('room_type')})", expanded=False):
                    st.json({
                        "bounds": rs.get("bounds"),
                        "signals": rs.get("signals"),
                        "objects": rs.get("objects", {}),
                    })

# Agents snapshots
st.subheader("World Agents")
for agent in world.agents:
    if hasattr(agent, "snapshot"):
        st.json(agent.snapshot())

# Scouts visualisation
st.subheader("Scouts — Local Grids")
show_occ = st.toggle("Show Occupancy (shape)", value=True)
show_sound = st.toggle("Show Sound grid", value=True)
show_light = st.toggle("Show Light grid", value=True)

scouts = getattr(world, "scouts", [])
if not scouts:
    st.info("No scouts present.")
else:
    for scout in scouts:
        snap = scout.snapshot()
        name = snap.get("name", "scout")
        frame = snap.get("frame", 0)
        with st.expander(f"{name} · frame {frame} · area {snap.get('area')}", expanded=True):
            st.json(snap)

            cols = st.columns(3)
            if show_occ:
                with cols[0]:
                    st.caption("Occupancy (Shape / Outline)")
                    fig, ax = plt.subplots()
                    ax.imshow(scout.occupancy, cmap="gray")
                    ax.axis("off")
                    st.pyplot(fig)

            if show_sound:
                with cols[1]:
                    st.caption("Sound Field")
                    fig, ax = plt.subplots()
                    ax.imshow(scout.sound, cmap="viridis")
                    ax.axis("off")
                    st.pyplot(fig)

            if show_light:
                with cols[2]:
                    st.caption("Light Field")
                    fig, ax = plt.subplots()
                    ax.imshow(scout.light, cmap="inferno")
                    ax.axis("off")
                    st.pyplot(fig)

# Investigator / ledger
st.subheader("Salience Investigator (Ledger)")
investigator = getattr(world, "salience_investigator", None)
if investigator is None:
    st.warning("No salience investigator present.")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Frames Processed", getattr(investigator, "frame_counter", 0))
        st.metric("Total Entries", len(getattr(investigator, "ledger", [])))
    with col2:
        st.json(investigator.snapshot())

    st.subheader("Recent Ledger Entries")
    ledger = getattr(investigator, "ledger", [])
    if ledger:
        st.json(ledger[-15:])
    else:
        st.write("Ledger is empty (advance world).")

    st.subheader("Detected Transitions (sound/light)")
    transitions = getattr(investigator, "transitions", [])
    if transitions:
        st.json(transitions[-15:])
    else:
        st.write("No transitions yet (wait for TV toggle).")

st.caption("Tip: Advance 20–40 steps. Walker returns to TV every 15 frames and toggles power → light/sound transitions appear.")