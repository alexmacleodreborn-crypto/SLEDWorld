import streamlit as st

st.set_page_config(layout="wide")
st.title("Neighbourhood — People & Streets")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world first.")
    st.stop()

st.subheader("People")
for p in world.people:
    st.json({
        "name": p.name,
        "age": p.age,
        "home": p.home_name,
        "position_xyz": p.position_xyz
    })

st.subheader("Streets / Places")
for name, place in world.places.items():
    if place.snapshot().get("type") in ("street", "neighbourhood"):
        st.json(place.snapshot())