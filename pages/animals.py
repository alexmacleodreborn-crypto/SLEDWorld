import streamlit as st

st.set_page_config(layout="wide")
st.title("Animals")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world first.")
    st.stop()

for a in world.animals:
    st.json({
        "name": a.name,
        "species": a.species,
        "color": a.color,
        "position_xyz": a.position_xyz
    })