import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

st.set_page_config(
    page_title="SLED World – A7DO Phase 1",
    layout="wide"
)

# -------------------------
# Session initialisation
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
cycle = st.session_state.cycle

# -------------------------
# Continuous physiology loop
# -------------------------

cycle.tick(dt=0.1)

# -------------------------
# Observer controls
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

# -------------------------
# Display
# -------------------------

st.title("A7DO — Phase 1 Physiology")

st.subheader("Physiology (Continuous)")
st.json(a7do.phys.snapshot())

st.subheader("State")
st.write("Awake:", a7do.is_awake)
st.write("Birthed:", a7do.birthed)

st.subheader("Internal Log (Sparse)")
st.code(
    "\n".join(a7do.internal_log[-30:])
    if a7do.internal_log else "—"
)