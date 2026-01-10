# pages/1_🌍_World_Map.py

st.title("World Map")

st.write(f"Frame: {world.frame}")

for place in world.places.values():
    st.json(place.snapshot())
st.caption("This is the world-first aerial reference. Everything else is downstream.")