import streamlit as st

st.set_page_config(layout="wide")
st.title("Manager — Gate Decisions")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world first.")
    st.stop()

st.subheader("Latest Manager Decision")
st.json(world.manager.snapshot())

st.subheader("Architect Plans")
st.json(world.architect.snapshot())

st.subheader("Builder Actions")
st.json(world.builder.snapshot())