import streamlit as st

st.set_page_config(layout="wide")
st.title("Symbol Learning — Pre-Language")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world first.")
    st.stop()

st.subheader("Concierge Proposals")
st.json(world.concierge.snapshot())

st.subheader("Language State")
st.json(world.language.snapshot())