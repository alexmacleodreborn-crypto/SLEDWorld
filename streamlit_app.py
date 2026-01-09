# streamlit_app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock


st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")


# ==================================================
# Session init
# ==================================================
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world


# ==================================================
# Sidebar
# ==================================================
st.sidebar.header("World Advancement")

advance_steps = st.sidebar.slider("Advance steps", 1, 50, 1)

if st.sidebar.button("▶ Advance World"):
    for _ in range(advance_steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()


# ==================================================
# Main
# ==================================================
st.title("SLEDWorld – Reality Frame")
st.caption("Reality first • Perception second • Accounting third • No clock awareness required")


# --------------------------
# World Space (Weather / Sky)
# --------------------------
st.subheader("World Space (Weather Fields)")

space = getattr(world, "space", None)
if space and hasattr(space, "snapshot"):
    ws = space.snapshot()
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.metric("Ambient Light", ws.get("ambient_light", 0.0))
        st.metric("Darkness", ws.get("darkness", 0.0))
    with colB:
        st.metric("Temp (°C)", ws.get("temperature_c", 0.0))
        st.metric("Cloud", ws.get("cloud", 0.0))
    with colC:
        st.metric("Wind", ws.get("wind_level", 0.0))
        st.metric("Rain", str(ws.get("rain", False)))
    with colD:
        st.metric("Snow", str(ws.get("snow", False)))
        st.metric("Frame", ws.get("frame", 0))
else:
    st.warning("No WorldSpace present.")


# --------------------------
# World State
# --------------------------
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
})


# --------------------------
# World Geometry & Objects
# --------------------------
st.subheader("World Geometry & Objects")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json({
            "position": getattr(place, "position", None),
            "bounds": getattr(place, "bounds", None),
        })

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                with st.expander(f"Room: {room.name}", expanded=False):
                    room_view = {
                        "bounds": getattr(room, "bounds", None),
                        "sound_level": getattr(room, "get_sound_level", lambda: None)(),
                        "objects": {},
                    }

                    if hasattr(room, "objects"):
                        for obj_name, obj in room.objects.items():
                            if hasattr(obj, "snapshot"):
                                room_view["objects"][obj_name] = obj.snapshot()
                            else:
                                # show TV state if present
                                d = {"repr": str(obj)}
                                if hasattr(obj, "is_on"):
                                    d["is_on"] = bool(getattr(obj, "is_on"))
                                if hasattr(obj, "position"):
                                    d["position"] = getattr(obj, "position")
                                room_view["objects"][obj_name] = d

                    st.json(room_view)


# --------------------------
# Observer Perception
# --------------------------
st.subheader("Observer Perception")

observer_found = False
for agent in world.agents:
    if agent.__class__.__name__ == "ObserverBot":
        observer_found = True
        st.json(agent.snapshot())

if not observer_found:
    st.warning("No observer present.")


# --------------------------
# Scouts (visual toggle)
# --------------------------
st.subheader("Scouts — Local Squares (Shape / Sound / Light)")

scouts = getattr(world, "scouts", [])
if not scouts:
    st.info("No scouts active.")
else:
    for s in scouts:
        snap = s.snapshot()
        with st.expander(f"{snap.get('name', 'Scout')} — frame {snap.get('frames', 0)}", expanded=True):
            st.json({
                "active": snap.get("active"),
                "target_room": snap.get("target_room"),
                "target_object": snap.get("target_object"),
                "sound_now": snap.get("sound_now"),
                "light_now": snap.get("light_now"),
                "darkness_now": snap.get("darkness_now"),
                "shape_persistence": snap.get("shape_persistence", 0),
            })

            show_shape = st.checkbox(f"Show shape grid — {snap.get('name','Scout')}", value=True, key=f"shape_{snap.get('name','scout')}")
            show_series = st.checkbox(f"Show series — {snap.get('name','Scout')}", value=True, key=f"series_{snap.get('name','scout')}")

            if show_shape:
                grid = snap.get("shape_grid")
                if grid:
                    arr = np.array(grid, dtype=float)
                    fig, ax = plt.subplots()
                    ax.imshow(arr, cmap="gray")
                    ax.set_title("Occupancy (Shape / Outline) — placeholder until surface scan wired")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No shape grid available.")

            if show_series:
                sound_tail = snap.get("sound_series_tail", [])
                light_tail = snap.get("light_series_tail", [])
                dark_tail = snap.get("darkness_series_tail", [])

                if sound_tail:
                    fig, ax = plt.subplots()
                    ax.plot(sound_tail)
                    ax.set_title("Sound tail (last ~10)")
                    st.pyplot(fig)

                if light_tail:
                    fig, ax = plt.subplots()
                    ax.plot(light_tail)
                    ax.set_title("Ambient light tail (last ~10)")
                    st.pyplot(fig)

                if dark_tail:
                    fig, ax = plt.subplots()
                    ax.plot(dark_tail)
                    ax.set_title("Darkness tail (last ~10)")
                    st.pyplot(fig)


# --------------------------
# World Agents
# --------------------------
st.subheader("World Agents")
for agent in world.agents:
    if hasattr(agent, "snapshot"):
        st.json(agent.snapshot())


# --------------------------
# Salience Investigator
# --------------------------
st.subheader("Salience Ledger (Accounting)")

investigator = getattr(world, "salience_investigator", None)
if investigator and hasattr(investigator, "snapshot"):
    inv_snap = investigator.snapshot()
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Frames (Accounting)", inv_snap.get("frame_counter", 0))
        st.metric("Total Transactions", inv_snap.get("total_transactions", 0))

    with col2:
        st.json(inv_snap)

    st.subheader("Recent Transactions (tail)")
    ledger = getattr(investigator, "ledger", [])
    if ledger:
        st.json(ledger[-10:])
    else:
        st.write("No transactions yet.")
else:
    st.warning("No salience investigator present.")


st.caption("Reality exists first • Global fields are sensed as coordinates • Meaning emerges from persistence")