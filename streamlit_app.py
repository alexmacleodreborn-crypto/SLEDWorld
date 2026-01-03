import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

# -------------------------------------------------
# Streamlit configuration
# -------------------------------------------------

st.set_page_config(
    page_title="SLED World – A7DO Cognitive Emergence",
    layout="wide"
)

# -------------------------------------------------
# Session initialisation
# -------------------------------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
cycle = st.session_state.cycle

# -------------------------------------------------
# Observer controls
# -------------------------------------------------

st.sidebar.header("Observer Control")

# ---------- PRE-BIRTH ----------

if not cycle.has_birthed:
    st.sidebar.subheader("Pre-birth phase")

    if st.sidebar.button("Run pre-birth cycle"):
        cycle.prebirth_cycle()

    st.sidebar.caption(
        f"Gestation cycles: {a7do.gestation_cycles} / 180"
    )

    st.sidebar.info(
        "A7DO is in womb perception.\n"
        "Wake/sleep cycles are muted.\n"
        "Birth unlocks awareness."
    )

# ---------- POST-BIRTH ----------

else:
    st.sidebar.subheader("Post-birth phase")

    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

    st.sidebar.divider()

    st.sidebar.subheader("Perception mode")

    modes = ["hospital", "home"]
    selected_mode = st.sidebar.selectbox(
        "A7DO perceived environment",
        modes,
        index=modes.index(a7do.perception_mode)
    )

    a7do.perception_mode = selected_mode

# -------------------------------------------------
# Main display
# -------------------------------------------------

st.title("🧠 A7DO – Cognitive Emergence")

st.subheader("A7DO Status")
st.write("Birthed:", a7do.birthed)
st.write("Awake:", a7do.is_awake)
st.write("Perception mode:", a7do.perception_mode)
st.write("Gestation cycles:", a7do.gestation_cycles)

st.divider()

st.subheader("Internal Log")
if a7do.internal_log:
    st.code("\n".join(a7do.internal_log))
else:
    st.write("—")

st.divider()

st.subheader("Familiarity (Pre-symbolic patterns)")
st.json(a7do.familiarity.top())