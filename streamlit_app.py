import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock


# ==================================================
# Streamlit config
# ==================================================
st.set_page_config(page_title="SLEDWorld – Pattern → Symbols → Language", layout="wide")


# ==================================================
# Session init (persist across reruns)
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world


# ==================================================
# Header + instructions
# ==================================================
st.title("SLEDWorld – Pattern → Symbols → Language")
st.caption(
    "Use **Advance** to step the world. The Manager reviews ledger events, applies Sandy-gating, "
    "and finalizes learning approvals."
)

colA, colB, colC = st.columns([1, 1, 2])

with colA:
    steps = st.number_input("Advance steps", min_value=1, max_value=200, value=5, step=1)
with colB:
    if st.button("▶ Advance"):
        for _ in range(int(steps)):
            clock.tick(minutes=1)
            world.tick()

with colC:
    if st.button("Reset world"):
        st.session_state.pop("world", None)
        st.session_state.pop("clock", None)
        st.rerun()


# ==================================================
# World state summary
# ==================================================
st.subheader("World State")
st.json({
    "frame": world.space.frame_counter,
    "weather": world.space.snapshot(),
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(world.scouts),
})


# ==================================================
# Aerial plot (places + agents)
# ==================================================
st.subheader("Aerial Plot")

fig, ax = plt.subplots(figsize=(7, 4))
ax.set_title(f"World frame: {world.space.frame_counter}")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(alpha=0.2)

# Places
for place in world.places.values():
    p = getattr(place, "position", None)
    b = getattr(place, "bounds", None)
    if p is not None:
        ax.scatter([p[0]], [p[1]])
        ax.text(p[0] + 5, p[1] + 5, place.name, fontsize=9)
    if b:
        (minx, miny, _), (maxx, maxy, _) = b
        rect_x = [minx, maxx, maxx, minx, minx]
        rect_y = [miny, miny, maxy, maxy, miny]
        ax.plot(rect_x, rect_y)

# Agents
for agent in world.agents:
    pos = getattr(agent, "position", None) or getattr(agent, "xyz", None)
    if pos:
        ax.scatter([pos[0]], [pos[1]], marker="x")
        ax.text(pos[0] + 5, pos[1] - 10, agent.name, fontsize=8)

st.pyplot(fig)


# ==================================================
# Objects (rooms, TV, remote)
# ==================================================
st.subheader("Places → Rooms → Objects")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json(place.snapshot() if hasattr(place, "snapshot") else {"name": place.name})

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                with st.expander(f"Room: {room.name}", expanded=False):
                    st.json(room.snapshot())


# ==================================================
# Bots (Observer, Walker, Scouts, Surveyor)
# ==================================================
st.subheader("Bots")

tabs = st.tabs(["Observer", "Walker", "Scouts", "Surveyor", "Manager", "Ledger"])

with tabs[0]:
    obs = world.get_agent("ObserverBot")
    if obs:
        st.json(obs.snapshot())
    else:
        st.warning("ObserverBot not found.")

with tabs[1]:
    walker = world.get_agent("WalkerBot")
    if walker:
        st.json(walker.snapshot())
    else:
        st.warning("WalkerBot not found.")

with tabs[2]:
    show_sound = st.checkbox("Show sound grid", value=True)
    show_light = st.checkbox("Show light grid", value=True)

    if not world.scouts:
        st.info("No scouts active.")
    for scout in world.scouts:
        snap = scout.snapshot()
        name = snap.get("name", "Scout")
        frame = snap.get("frame", "?")
        with st.expander(f"{name} · frame {frame}", expanded=False):
            st.json({k: v for k, v in snap.items() if k not in ("sound_grid", "light_grid", "occupancy")})

            if show_sound and "sound_grid" in snap and snap["sound_grid"] is not None:
                st.write("Sound grid")
                st.image(np.array(snap["sound_grid"], dtype=np.float32), clamp=True)

            if show_light and "light_grid" in snap and snap["light_grid"] is not None:
                st.write("Light grid")
                st.image(np.array(snap["light_grid"], dtype=np.float32), clamp=True)

            if "occupancy" in snap and snap["occupancy"] is not None:
                st.write("Occupancy (shape)")
                st.image(np.array(snap["occupancy"], dtype=np.float32), clamp=True)

with tabs[3]:
    if world.surveyor:
        snap = world.surveyor.snapshot()
        st.json({k: v for k, v in snap.items() if k not in ("volume", "surface_volume")})

        # cheap aerial occupancy: sum along z
        if "volume" in snap and snap["volume"] is not None:
            vol = np.array(snap["volume"], dtype=np.int8)
            aerial = vol.sum(axis=0)
            st.write("Surveyor aerial occupancy (sum over Z)")
            st.image(aerial, clamp=True)
    else:
        st.warning("Surveyor not present.")

with tabs[4]:
    st.json(world.manager.snapshot())
    st.write("Approvals")
    st.json(world.manager.approvals[-20:])

with tabs[5]:
    st.metric("Ledger events", len(world.ledger.events))
    st.json(world.ledger.events[-20:] if world.ledger.events else [])