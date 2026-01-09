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
    # Clock is now observational, not causal
    st.session_state.clock = WorldClock(acceleration=1)

clock = st.session_state.clock

if "world" not in st.session_state:
    st.session_state.world = build_world(clock)

world = st.session_state.world

# ==================================================
# Sidebar – World Advancement
# ==================================================
st.sidebar.header("World Advancement")

advance_reason = st.sidebar.selectbox(
    "Advance reason",
    [
        "structural_change",
        "agent_interaction",
        "external_event",
        "observation_only",
    ]
)

advance_steps = st.sidebar.slider(
    "Advance intensity",
    1, 5, 1
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        # World decides what changes
        changed = world.advance(reason=advance_reason)

        # Only tick clock if something actually changed
        if changed:
            clock.annotate(event=advance_reason)

st.sidebar.divider()

st.sidebar.caption(
    "World advances only when change occurs.\n"
    "Time is recorded, not enforced."
)

# ==================================================
# Main Display
# ==================================================
st.title("SLEDWorld – Reality Frame")

# --------------------------
# World State (Primary)
# --------------------------
st.subheader("World State")
st.json(world.snapshot())

# --------------------------
# World Time (Secondary)
# --------------------------
st.subheader("World Time (Derived)")
st.json(clock.snapshot())

st.caption(
    "World time is a record of change, not a driver."
)

# --------------------------
# World Grid
# --------------------------
st.subheader("World Grid")
st.json(world.grid.snapshot())

# --------------------------
# World Summary
# --------------------------
st.subheader("World Summary")
st.json({
    "num_places": len(world.places),
    "place_names": list(world.places.keys()),
    "num_agents": len(world.agents),
})

# --------------------------
# World Places
# --------------------------
st.subheader("World Places")

for name, place in world.places.items():
    with st.expander(name, expanded=False):
        st.json(place.snapshot())

# --------------------------
# World Agents
# --------------------------
st.subheader("World Agents")

if not world.agents:
    st.write("No active agents.")
else:
    for agent in world.agents:
        st.json(agent.snapshot())

# ==================================================
# Footer
# ==================================================
st.caption(
    "This view represents the objective world frame. "
    "Reality progresses via change, not scheduled time."
)