import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")

# --------------------
# Session init (ONLY place build_world is called)
# --------------------
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# --------------------
# Sidebar
# --------------------
st.sidebar.header("World Control")

advance_steps = st.sidebar.slider("Advance frames", 1, 50, 1)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

if st.sidebar.button("Reset World"):
    st.session_state.clear()
    st.rerun()

# --------------------
# Helpers: rasterize bounds into a small grid
# --------------------
def world_bounds():
    xs, ys, zs = [], [], []
    for p in world.places.values():
        b = getattr(p, "bounds", None)
        if b:
            (min_x, min_y, min_z), (max_x, max_y, max_z) = b
            xs += [min_x, max_x]
            ys += [min_y, max_y]
            zs += [min_z, max_z]
        if hasattr(p, "rooms"):
            for r in p.rooms.values():
                b = getattr(r, "bounds", None)
                if b:
                    (min_x, min_y, min_z), (max_x, max_y, max_z) = b
                    xs += [min_x, max_x]
                    ys += [min_y, max_y]
                    zs += [min_z, max_z]
    if not xs:
        return (0, 0, 0), (100, 100, 10)
    pad = 5.0
    return (min(xs)-pad, min(ys)-pad, min(zs)), (max(xs)+pad, max(ys)+pad, max(zs))

def to_grid_xy(x, y, min_x, min_y, scale):
    gx = int((x - min_x) * scale)
    gy = int((y - min_y) * scale)
    return gx, gy

# --------------------
# Main
# --------------------
st.title("SLEDWorld – Reality Frame")

frame_guess = None
for a in world.agents:
    if hasattr(a, "snapshot"):
        s = a.snapshot()
        if isinstance(s, dict) and "frame" in s:
            frame_guess = s["frame"]
            break

st.metric("World Frame", frame_guess if frame_guess is not None else "N/A")

# --------------------
# Aerial (Top-down) Plot
# --------------------
st.subheader("🛰 Aerial Plot (Top-Down)")

(min_x, min_y, min_z), (max_x, max_y, max_z) = world_bounds()

# low-cost grid for plotting
W = 220
H = 220
scale = (W - 1) / max(1e-6, (max_x - min_x))

canvas = np.zeros((H, W), dtype=np.uint8)

# draw places + rooms as outlines
fig, ax = plt.subplots()

# Places
for place in world.places.values():
    b = getattr(place, "bounds", None)
    if not b:
        continue
    (x1, y1, _), (x2, y2, _) = b
    ax.plot([x1, x2, x2, x1, x1],
            [y1, y1, y2, y2, y1], linewidth=1)

    # Rooms
    if hasattr(place, "rooms"):
        for room in place.rooms.values():
            rb = getattr(room, "bounds", None)
            if not rb:
                continue
            (rx1, ry1, _), (rx2, ry2, _) = rb
            ax.plot([rx1, rx2, rx2, rx1, rx1],
                    [ry1, ry1, ry2, ry2, ry1], linewidth=0.8)

            # TV marker
            tv = getattr(room, "objects", {}).get("tv")
            if tv and hasattr(tv, "position") and room.room_type == "living_room":
                tx, ty, tz = tv.position
                lv = tv.light_level() if hasattr(tv, "light_level") else {"color": "white"}
                ax.scatter([tx], [ty], s=60, marker="s")
                ax.text(tx, ty, f"TV({lv.get('color')})", fontsize=8)

# Agents
for agent in world.agents:
    if hasattr(agent, "position"):
        x, y, z = agent.position
        ax.scatter([x], [y], s=40)
        ax.text(x, y, getattr(agent, "name", "agent"), fontsize=8)

ax.set_aspect("equal", adjustable="box")
ax.set_title("Places / Rooms / TV / Agents")
ax.set_xlabel("X")
ax.set_ylabel("Y")
st.pyplot(fig)

# --------------------
# Simple 3D Impression (Z slices)
# --------------------
st.subheader("🧊 Simple 3D Impression (3 Z-Slices)")

# Create occupancy at three heights based on bounds containment
z_slices = [
    min_z + 0.5,
    min_z + 1.5,
    min_z + 2.5,
]

grid_size = 140
scale3 = (grid_size - 1) / max(1e-6, (max_x - min_x))
imps = []

for z0 in z_slices:
    occ = np.zeros((grid_size, grid_size), dtype=np.uint8)

    for iy in range(grid_size):
        y = min_y + iy / scale3
        for ix in range(grid_size):
            x = min_x + ix / scale3
            solid = False
            # room containment first
            for place in world.places.values():
                if hasattr(place, "rooms"):
                    for room in place.rooms.values():
                        if room.contains_world_point((x, y, z0)):
                            solid = True
                            break
                if solid:
                    break
                if place.contains_world_point((x, y, z0)):
                    solid = True
                    break
            occ[iy, ix] = 255 if solid else 0

    imps.append(occ)

c1, c2, c3 = st.columns(3)
for col, occ, z0 in zip([c1, c2, c3], imps, z_slices):
    with col:
        st.write(f"Z ≈ {z0:.2f}m")
        fig, ax = plt.subplots()
        ax.imshow(occ, cmap="gray", origin="lower")
        ax.axis("off")
        st.pyplot(fig)

# --------------------
# Object + room detail (lightweight)
# --------------------
st.subheader("🏠 Living Room Detail (TV / Remote)")

for place in world.places.values():
    if not hasattr(place, "rooms"):
        continue
    for room in place.rooms.values():
        if getattr(room, "room_type", "") != "living_room":
            continue
        st.json({
            "room": room.name,
            "bounds": getattr(room, "bounds", None),
            "sound_level": room.get_sound_level() if hasattr(room, "get_sound_level") else None,
            "light": room.get_light_level() if hasattr(room, "get_light_level") else None,
            "objects": {
                k: (v.snapshot() if hasattr(v, "snapshot") else str(v))
                for k, v in getattr(room, "objects", {}).items()
            }
        })

st.caption("Reality exists first • You are now visualising it without heavy 3D grids.")