import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from world_core.mother_bot import MotherBot
from a7do_core.gestation_bridge import GestationBridge

st.set_page_config(page_title="SLED World – A7DO", layout="wide")

# -------------------------
# Session init
# -------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()
    st.session_state.mother = MotherBot()
    st.session_state.gestation = GestationBridge(
        st.session_state.mother,
        st.session_state.a7do
    )
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
mother = st.session_state.mother
gestation = st.session_state.gestation
cycle = st.session_state.cycle

# -------------------------
# Continuous loop
# -------------------------

dt = 0.1
mother.tick(dt)
gestation.tick(dt)
cycle.tick(dt)

# -------------------------
# Controls
# -------------------------

st.sidebar.header("Observer")

if not a7do.birthed:
    if st.sidebar.button("Trigger Birth"):
        gestation.end_gestation()
        cycle.ensure_birth()
else:
    if st.sidebar.button("Wake"):
        cycle.wake()
    if st.sidebar.button("Sleep"):
        cycle.sleep()

# -------------------------
# Display
# -------------------------

st.title("A7DO — Pre-birth Mother Coupling")

st.subheader("Mother Physiology")
st.json(mother.snapshot())

st.subheader("A7DO Physiology")
st.json(a7do.phys.snapshot())

st.subheader("Internal Log")
st.code("\n".join(a7do.internal_log[-30:]) if a7do.internal_log else "—")