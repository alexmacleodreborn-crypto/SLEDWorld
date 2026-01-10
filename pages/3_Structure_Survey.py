import streamlit as st

st.set_page_config(layout="wide")
st.title("Structure Survey — Geometry")

world = st.session_state.get("world")
if not world or not world.surveyor:
    st.warning("Surveyor not active.")
    st.stop()

snap = world.surveyor.snapshot()
st.json(snap)

st.caption("Voxel-based solid and surface detection (pre-language)")