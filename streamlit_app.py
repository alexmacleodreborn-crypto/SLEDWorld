import streamlit as st

# ---------- Core imports ----------
from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_frame.world_controller import WorldController

# ---------- Page config ----------
st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide",
)

st.title("🧠 SLED World – A7DO Cognitive Emergence")

# ---------- Session State ----------
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "world" not in st.session_state:
    st.session_state.world = WorldController()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(
        a7do=st.session_state.a7do,
        world=st.session_state.world,
    )

a7do = st.session_state.a7do
world = st.session_state.world
cycle = st.session_state.cycle

# ---------- Layout ----------
col_control, col_state, col_log = st.columns([1.2, 1.2, 2.2])

# =====================================================================
# CONTROL PANEL
# =====================================================================
with col_control:
    st.subheader("🎛 Observer Controls")

    if not a7do.birthed:
        st.info("A7DO not yet birthed.")
        if st.button("👶 Begin Birth Event"):
            cycle.ensure_birth()
    else:
        st.success("A7DO birthed")

    st.divider()

    st.write("**Awake Experience Window**")
    ticks = st.number_input(
        "Awake ticks (continuous sensory feed)",
        min_value=5,
        max_value=200,
        value=20,
        step=5,
    )

    if st.button("▶ Run Awake Window"):
        cycle.run_day_window(n_ticks=int(ticks))

    if st.button("🌙 Sleep → Next Day"):
        cycle.sleep_and_advance()

# =====================================================================
# A7DO INTERNAL STATE
# =====================================================================
with col_state:
    st.subheader("🧍 A7DO Internal State")

    st.write(f"**Day:** {a7do.day}")
    st.write(f"**Awake:** {cycle.awake}")
    st.write(f"**Perceived Place:** {a7do.perceived.current_place}")

    st.divider()

    st.write("**Body Drives**")
    st.progress(a7do.body.hunger, text=f"Hunger: {a7do.body.hunger:.2f}")
    st.progress(a7do.body.wetness, text=f"Wetness: {a7do.body.wetness:.2f}")
    st.progress(a7do.body.fatigue, text=f"Fatigue: {a7do.body.fatigue:.2f}")

    st.divider()

    st.write("**Familiarity (Top Patterns)**")
    for pattern, score in a7do.familiarity.top(5):
        st.write(f"- {pattern}: {score:.2f}")

# =====================================================================
# OBSERVER LOG
# =====================================================================
with col_log:
    st.subheader("📜 Observer Log (Live)")

    if not a7do.log.entries:
        st.info("No experiences yet.")
    else:
        for entry in reversed(a7do.log.entries[-50:]):
            st.write(entry)

# =====================================================================
# WORLD SNAPSHOT (DEBUG / TRANSPARENCY)
# =====================================================================
with st.expander("🌍 World Snapshot (Observer View)"):
    st.json(world.snapshot())