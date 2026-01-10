import streamlit as st

st.set_page_config(layout="wide")
st.title("Ledger Inspector")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world first.")
    st.stop()

st.subheader("Ledger Metrics (Sandy’s Law)")
st.json(world.ledger.snapshot())

st.subheader("Recent Ledger Events")
st.json(world.ledger.tail(50))