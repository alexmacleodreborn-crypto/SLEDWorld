import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

st.set_page_config(
    page_title="SLED World – A7DO",
    layout="wide"
)

# -------------------------
# Session initialisation
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
cycle = st.session_state.cycle

# -------------------------
# Observer Control
# -------------------------

st.sidebar.header("Observer Control")

if not cycle.has_birthed:
    if st.sidebar.button("Trigger Birth"):
        cycle.ensure_birth()
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

# Perception selector (only AFTER birth)
if a7do.birthed:
    modes = ["hospital", "home"]
    selected = st.sidebar.selectbox(
        "A7DO perception mode",
        modes,
        index=modes.index(a7do.perception_mode)
    )
    a7do.perception_mode = selected
else:
    st.sidebar.info("Pre-birth: perception locked to womb")

# -------------------------
# Display
# -------------------------

st.title("A7DO Cognitive Emergence")

st.subheader("A7DO Status")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perception mode:", a7do.perception_mode)

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log) if a7do.internal_log else "—")

st.subheader("Familiarity (Top Patterns)")
st.json(a7do.familiarity.top())