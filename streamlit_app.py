import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_frame.world_controller import WorldController

st.set_page_config(
    page_title="SLED World – Observer",
    layout="wide"
)

st.title("🌍 SLED World")
st.caption("Observer-controlled developmental reality")

# --------------------------------------------------
# Session bootstrap
# --------------------------------------------------
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "world" not in st.session_state:
    st.session_state.world = WorldController()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(
        a7do=st.session_state.a7do,
        world=st.session_state.world
    )

a7do = st.session_state.a7do
world = st.session_state.world
cycle = st.session_state.cycle

# --------------------------------------------------
# Controls (Observer only)
# --------------------------------------------------
st.subheader("Observer Controls")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🍼 Birth"):
        cycle.ensure_birth()

with c2:
    if st.button("🌞 Wake"):
        cycle.wake()

with c3:
    if st.button("▶ Run Day Window"):
        cycle.run_day_window()

with c4:
    if st.button("🌙 Sleep → Next Day"):
        cycle.sleep_and_advance()

# --------------------------------------------------
# Status
# --------------------------------------------------
st.divider()
left, right = st.columns(2)

with left:
    st.subheader("A7DO (Perceived)")
    st.json({
        "birthed": a7do.birthed,
        "day": a7do.day_index,
        "current_place": a7do.perceived.current_place,
    })

    st.subheader("Familiarity (Top Patterns)")
    st.table(a7do.familiarity.top(10))

with right:
    st.subheader("SLED World (Objective)")
    st.json(world.snapshot())

# --------------------------------------------------
# Internal log (pre-language)
# --------------------------------------------------
st.divider()
st.subheader("Internal Log")
st.code("\n".join(a7do.log.tail(60)))