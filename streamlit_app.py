import streamlit as st

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

# ==================================================
# Streamlit config
# ==================================================
st.set_page_config(
    page_title="SLEDWorld — Manager Overview",
    layout="wide",
)

# ==================================================
# Canonical session bootstrap (DO NOT DUPLICATE)
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

world = st.session_state.world
clock = st.session_state.clock

# ==================================================
# HEADER
# ==================================================
st.title("🧠 SLEDWorld — Manager & Gatekeeper")

st.caption(
    "World-first intelligence • Patterns → Structure → Meaning • "
    "All cognition is downstream of reality."
)

# ==================================================
# WORLD CONTROL (ONLY PLACE THAT TICKS)
# ==================================================
st.divider()
st.subheader("World Control")

colA, colB = st.columns([1, 2])

with colA:
    steps = st.number_input(
        "Advance steps",
        min_value=1,
        max_value=50,
        value=1,
        step=1,
    )

with colB:
    if st.button("▶ Advance World"):
        for _ in range(int(steps)):
            world.tick()

# ==================================================
# GLOBAL STATUS
# ==================================================
st.divider()
st.subheader("Global World Status")

status_cols = st.columns(4)

status_cols[0].metric("Frame", world.frame)
status_cols[1].metric("Places", len(world.places))
status_cols[2].metric("Agents", len(world.agents))
status_cols[3].metric(
    "Ledger Events",
    len(world.ledger.events) if hasattr(world, "ledger") else 0,
)

# ==================================================
# MANAGER SUMMARY (TOP-DOWN)
# ==================================================
st.divider()
st.subheader("Manager Summary")

summary = {
    "places": list(world.places.keys()),
    "agents": [a.name for a in world.agents],
    "scouts": len(getattr(world, "scouts", [])),
    "ledger_events": len(world.ledger.events),
    "stable_symbols": getattr(world.ledger, "stable_symbols", []),
}

st.json(summary)

# ==================================================
# SANDY’S LAW GATING (DECISION LOGIC)
# ==================================================
st.divider()
st.subheader("Sandy’s Law — Gating & Validation")

gate_cols = st.columns(3)

with gate_cols[0]:
    st.metric(
        "Pattern Stability",
        world.ledger.pattern_stability_score(),
    )

with gate_cols[1]:
    st.metric(
        "Structural Confidence",
        world.ledger.structure_confidence_score(),
    )

with gate_cols[2]:
    st.metric(
        "Semantic Readiness",
        world.ledger.semantic_readiness_score(),
    )

st.caption(
    "Gates open only when repeated, cross-modal evidence converges.\n"
    "No single bot can promote meaning."
)

# ==================================================
# ACTIVE BOT OVERVIEW
# ==================================================
st.divider()
st.subheader("Active Bots")

for agent in world.agents:
    with st.expander(f"🤖 {agent.name}", expanded=False):
        if hasattr(agent, "snapshot"):
            st.json(agent.snapshot())
        else:
            st.write("No snapshot available.")

# ==================================================
# SCOUT STATUS
# ==================================================
st.divider()
st.subheader("Scout Activity")

scouts = getattr(world, "scouts", [])
if not scouts:
    st.write("No active scouts.")
else:
    for scout in scouts:
        with st.expander(f"🔍 {scout.name}", expanded=False):
            st.json(scout.snapshot())

# ==================================================
# LEDGER — RECENT TRANSACTIONS
# ==================================================
st.divider()
st.subheader("Ledger — Recent Events")

ledger_events = world.ledger.events[-20:]

if not ledger_events:
    st.write("Ledger empty.")
else:
    for event in ledger_events[::-1]:
        with st.expander(
            f"Frame {event['frame']} · {event['source']}",
            expanded=False,
        ):
            st.json(event)

# ==================================================
# MANAGER APPROVALS
# ==================================================
st.divider()
st.subheader("Manager Approvals")

approvals = world.ledger.pending_approvals()

if not approvals:
    st.success("No pending approvals.")
else:
    for approval in approvals:
        st.warning(f"Pending: {approval}")

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.caption(
    "This page does not perceive. It does not learn. It governs.\n"
    "Reality → Observation → Ledger → Gates → Meaning."
)