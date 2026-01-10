# streamlit_app.py

import streamlit as st
from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLEDWorld – Layered Reality", layout="wide")

# -------------------------
# Session init
# -------------------------
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("World Advancement")

advance_steps = st.sidebar.slider("Advance steps", 1, 50, 5)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World (hard)"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

# -------------------------
# Home
# -------------------------
st.title("SLEDWorld — Layered Reality")
st.caption("World-first → perception → salience → ledger → symbols → language")

st.subheader("Current World Summary")
st.json({
    "frame": getattr(world, "frame", None),
    "num_places": len(getattr(world, "places", {})),
    "num_agents": len(getattr(world, "agents", [])),
    "num_scouts": len(getattr(world, "scouts", [])),
    "ledger_entries": len(getattr(getattr(world, "salience_investigator", None), "ledger", []))
                     if getattr(world, "salience_investigator", None) else 0,
})

st.info("Use the left sidebar to advance. Use the Pages menu to inspect each layer.")