# pages/1_🌍_World_Map.py

import streamlit as st
import matplotlib.pyplot as plt

st.title("🌍 World Map (Aerial 2D)")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

places = getattr(world, "places", {})

# Collect bounds/positions
pts = []
boxes = []
for name, place in places.items():
    pos = getattr(place, "position", None)
    b = getattr(place, "bounds", None)
    if pos:
        pts.append((name, pos))
    if b:
        boxes.append((name, b))

st.subheader("Places")
st.write(list(places.keys()))

st.subheader("Aerial Plot")
fig, ax = plt.subplots()

# Plot bounds (rectangles) if present
for name, bounds in boxes:
    (min_x, min_y, _), (max_x, max_y, _) = bounds
    ax.plot([min_x, max_x, max_x, min_x, min_x],
            [min_y, min_y, max_y, max_y, min_y])

# Plot positions
for name, (x, y, _z) in pts:
    ax.scatter([x], [y])
    ax.text(x, y, f" {name}", fontsize=8)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title(f"World frame: {getattr(world, 'frame', '?')}")
st.pyplot(fig)

st.caption("This is the world-first aerial reference. Everything else is downstream.")