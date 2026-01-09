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
# Session initialisation (ORDER MATTERS)
# ==================================================
if "clock" not in st.session_state:
    # Clock exists but does NOT drive the world
    st.session_state.clock = WorldClock(acceleration=1)

clock = st.session_state.clock

if "world" not in st.session_state:
    st.session_state.world = build_world(clock)

world = st.session_state.world

# ==================================================
# Sidebar – World Advancement (Change-driven)
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
    min_value=1,
    max_value=5,
    value=1,
)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        # 1️⃣ Advance time explicitly (minutes)
        clock.tick(minutes=1)

        # 2️⃣ Advance world physics
        world.tick()

        # 3️⃣ Allow observers to perceive
        for agent in world.agents:
            if hasattr(agent, "observe"):
                agent.observe(world)
                
st.sidebar.divider()
st.sidebar.caption(
    "World advances via change, not scheduled time.\n"
    "Clock is present but non-authoritative."
)

# ==================================================
# Main Display
# ==================================================
st.title("SLEDWorld – Reality Frame")

# --------------------------
# World State (Primary)
# --------------------------
st.subheader("World State")
st.json({
    "num_places": len(world.places),
    "place_names": list(world.places.keys()),
    "num_agents": len(world.agents),
})

# --------------------------
# World Time (Derived / Secondary)
# --------------------------
st.subheader("World Time (Secondary)")
st.json(clock.snapshot())

st.caption(
    "World time is a record, not a cause."
)

# --------------------------
# World Grid
# --------------------------
st.subheader("World Grid")
st.json(world.grid.snapshot())

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
# Observer View (Perception / Reality)
# ==================================================
st.subheader("Observer Perception")

observer_found = False

for agent in world.agents:
    if agent.__class__.__name__ == "ObserverBot":
        observer_found = True

        st.json({
            "observer": agent.name,
            "frames_observed": agent.frames_observed,
            "persistent_places": agent.seen_places,
        })

if not observer_found:
    st.info("No observer agent present.")

# ==================================================
# Footer
# ==================================================
st.caption(
    "This view represents the objective world frame.\n"
    "Reality persists independently of agents and schedules."
)