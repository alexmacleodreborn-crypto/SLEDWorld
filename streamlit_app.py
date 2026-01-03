import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.event_applier import apply_event

from world_core.world_state import WorldState
from world_core.intersection_gate import perceived_snapshot

from experience_layer.experience_generator import ExperienceGenerator

st.set_page_config(page_title="SLED World – A7DO", layout="wide")


# -------------------------
# Session init
# -------------------------
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

if "gen" not in st.session_state:
    st.session_state.gen = ExperienceGenerator()

a7do = st.session_state.a7do
world = st.session_state.world
cycle = st.session_state.cycle
gen = st.session_state.gen


# -------------------------
# World always runs
# -------------------------
world.tick(0.25)  # ~15 mins per UI refresh (conceptual)


# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("Observer Control")

steps = st.sidebar.slider("Experience steps per run", 1, 60, 12)
dt = st.sidebar.slider("Step dt", 0.05, 1.0, 0.25)

if not cycle.has_birthed:
    if st.sidebar.button("Trigger Birth"):
        cycle.ensure_birth()
else:
    c1, c2, c3 = st.sidebar.columns(3)
    if c1.button("Wake"):
        cycle.wake()

    if c2.button("Run Experience"):
        # Run micro experiences (prebirth drift already handled; postbirth only while awake)
        def provider():
            return perceived_snapshot(world, a7do)

        events = gen.run_block(a7do=a7do, perceived_provider=provider, steps=steps, dt=dt)
        for ev in events:
            apply_event(a7do, ev)

    if c3.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

st.sidebar.divider()

# Place toggle (for quick testing)
st.sidebar.subheader("Place (World)")
place = st.sidebar.selectbox("Current place", ["hospital", "home"], index=0 if world.current_place == "hospital" else 1)
world.set_place(place)


# -------------------------
# Main display
# -------------------------
st.title("SLED World — A7DO Cognitive Emergence")

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("World State")
    st.json(
        {
            "t": round(world.t, 3),
            "place": world.current_place,
            "ambient": round(world.ambient_level(), 3),
            "light": round(world.light_level(), 3),
            "sound": round(world.sound_level(), 3),
            "bots": [{"name": b.name, "role": b.role, "x": round(b.x, 2), "y": round(b.y, 2)} for b in world.bots],
        }
    )

    st.subheader("Perceived Snapshot (Intersection Gate)")
    st.json(perceived_snapshot(world, a7do))

with colB:
    st.subheader("A7DO State")
    st.json(
        {
            "day": cycle.day,
            "has_birthed": cycle.has_birthed,
            "a7do_birthed": a7do.birthed,
            "prebirth": getattr(a7do, "prebirth", False),
            "awake": a7do.is_awake,
        }
    )

    st.subheader("Internal Log")
    st.code("\n".join(a7do.internal_log[-40:]) if a7do.internal_log else "—")

    st.subheader("Top Familiarity Patterns")
    st.json(a7do.familiarity.top(8))