import streamlit as st

st.set_page_config(layout="wide")
st.title("World Map — Aerial Overview")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world from the Manager page.")
    st.stop()

st.subheader("Places")
for name, place in world.places.items():
    st.json(place.snapshot())

st.subheader("World Space / Weather")
st.json(world.space.snapshot())