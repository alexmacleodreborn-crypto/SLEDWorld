import streamlit as st
import matplotlib.pyplot as plt

st.title("World Map")

world = st.session_state.get("world")
if not world:
    st.warning("No world in session. Go to main page first.")
    st.stop()

occ = world.grid.render_occupancy(size=96)
fig, ax = plt.subplots()
ax.imshow(occ, interpolation="nearest")
ax.axis("off")
st.pyplot(fig, use_container_width=True)

st.subheader("Places")
st.json(list(world.places.keys()))