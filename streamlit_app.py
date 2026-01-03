import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.gestation_bridge import GestationBridge
from world_core.mother_bot import MotherBot

st.set_page_config(
    page_title="SLED World – A7DO",
    layout="wide"
)

# -------------------------
# SESSION STATE (HARD SAFE)
# -------------------------

if "a7do" not in st.session_state:
    st.session_state["a7do"] = A7DOState()

if "mother" not in st.session_state:
    st.session_state["mother"] = MotherBot()

if "gestation" not in st.session_state:
    st.session_state["gestation"] = GestationBridge(
        st.session_state["mother"],
        st.session_state["a7do"]
    )

if "cycle" not in st.session_state:
    st.session_state["cycle"] = DayCycle(st.session_state["a7do"])

# -------------------------
# LOCAL REFERENCES
# -------------------------

a7do = st.session_state["a7do"]
mother = st.session_state["mother"]
gestation = st.session_state["gestation"]
cycle = st.session_state["cycle"]

# -------------------------
# CONTINUOUS TIME LOOP
# -------------------------

dt = 0.1
mother.tick(dt)
gestation.tick(dt)
cycle.tick(dt)

# -------------------------
# OBSERVER CONTROLS
# -------------------------

st.sidebar.header("Observer Control")

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
# DISPLAY
# -------------------------

st.title("A7DO — Mother Coupling Phase")

st.subheader("Mother Physiology")
st.json(mother.snapshot())

st.subheader("A7DO Physiology")
st.json(a7do.phys.snapshot())

st.subheader("A7DO State")
st.write("Awake:", a7do.is_awake)
st.write("Birthed:", a7do.birthed)

st.subheader("Internal Log")
st.code(
    "\n".join(a7do.internal_log[-30:])
    if a7do.internal_log else "—"
)