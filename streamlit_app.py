import streamlit as st

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
    "Advance frames",
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
    "frame": world.frame,
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(world.scouts),
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
                    st.json(room.snapshot())

# --------------------------
# Agents (Walker / Observer)
# --------------------------
st.subheader("World Agents")

for agent in world.agents:
    if hasattr(agent, "snapshot"):
        st.json(agent.snapshot())

# --------------------------
# Scouts (Sound / Light)
# --------------------------
st.subheader("Scouts")

if world.scouts:
    for scout in world.scouts:
        snap = scout.snapshot()
        if snap:
            st.json(snap)
else:
    st.write("No active scouts.")

# --------------------------
# Surveyor (Geometry)
# --------------------------
st.subheader("Surveyor")

if world.surveyor:
    st.json(world.surveyor.snapshot())
else:
    st.write("No surveyor present.")

# --------------------------
# Ledger (Sandy’s Law Gate)
# --------------------------
st.subheader("Ledger (Accounting Layer)")

ledger = world.ledger

st.metric("Frames Recorded", ledger.frame_counter)
st.metric("Total Events", len(ledger.events))

with st.expander("Recent Ledger Events", expanded=False):
    st.json(ledger.events[-15:])

# --------------------------
# Architect
# --------------------------
st.subheader("Architect (Pattern Recognition)")
st.json(world.architect.snapshot())

# --------------------------
# Builder
# --------------------------
st.subheader("Builder (Structure Confirmation)")
st.json(world.builder.snapshot())

# --------------------------
# Language
# --------------------------
st.subheader("Language (Symbol Binding)")
st.json(world.language.snapshot())

# --------------------------
# Weather (Placeholder – correct for now)
# --------------------------
st.subheader("World Conditions")

st.json({
    "weather": "clear",
    "light_cycle": "static",
    "wind": "none",
    "note": "World conditions not yet active (pre-A7DO)",
})

# ==================================================
# Footer
# ==================================================
st.caption(
    "Reality exists first. "
    "Perception follows. "
    "Structure emerges. "
    "Language is grounded. "
    "A7DO not yet born."
)