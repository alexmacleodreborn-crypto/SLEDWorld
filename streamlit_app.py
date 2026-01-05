import streamlit as st
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world


# ======================================================
# Streamlit config
# ======================================================

st.set_page_config(
    page_title="SLED World – World Frame",
    layout="wide",
)


# ======================================================
# Session initialisation
# ======================================================

if "world" not in st.session_state:
    st.session_state.world = build_world()

world = st.session_state.world


# ======================================================
# CLOCK ACCESS (robust)
# ======================================================

# Support both object-style and dict-style worlds
if hasattr(world, "clock"):
    clock = world.clock
else:
    clock = world.clock


# ======================================================
# World clock control (OBSERVER)
# ======================================================

st.sidebar.header("World Clock")

accel = st.sidebar.slider(
    "Time acceleration (world seconds per real second)",
    min_value=1,
    max_value=3600,
    value=getattr(clock, "acceleration", 60),
    step=1,
)

clock.acceleration = accel

step_real_seconds = st.sidebar.slider(
    "Step (real seconds)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1,
)


# ======================================================
# World tick (SAFE)
# ======================================================

# Advance world time
clock.tick(real_seconds=step_real_seconds)

# Advance world systems (if method exists)
if hasattr(world, "tick"):
    world.tick()


# ======================================================
# WORLD MAP RENDERER
# ======================================================

def render_world_map(world):
    fig, ax = plt.subplots(figsize=(8, 8))

    places = world.places if hasattr(world, "places") else world["places"]

    for name, place in places.items():
        b = place.bounds

        x0, x1 = b["x"]
        y0, y1 = b["y"]

        width = x1 - x0
        height = y1 - y0

        ax.add_patch(
            plt.Rectangle(
                (x0, y0),
                width,
                height,
                fill=False,
                linewidth=2,
            )
        )

        ax.text(
            x0 + width / 2,
            y0 + height / 2,
            name,
            ha="center",
            va="center",
            fontsize=9,
        )

    ax.set_title("World Map (Top-Down XY Projection)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)

    return fig


# ======================================================
# DISPLAY
# ======================================================

st.title("SLED World – World Frame")

st.subheader("World Time")
st.json(clock.snapshot())


st.subheader("World Places")
places = world.places if hasattr(world, "places") else world["places"]

for name, place in places.items():
    st.markdown(f"### {name}")
    st.json(place.snapshot())


st.subheader("World Map")
fig = render_world_map(world)
st.pyplot(fig)


st.caption(
    "Observer-only world frame. "
    "No agents. No perception. No Sandy’s Law gating yet."
)