import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock


st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")


# Session init
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world


# Sidebar
st.sidebar.header("World Advancement")
steps = st.sidebar.slider("Advance frames", 1, 50, 1)

if st.sidebar.button("▶ Advance World"):
    for _ in range(steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()

if st.sidebar.button("Reset World"):
    st.session_state.clear()
    st.rerun()


# Main
st.title("SLEDWorld – Reality Frame")
st.caption("Reality first • Fields and surfaces • Meaning can emerge later")


# Weather / WorldSpace
st.subheader("World Space (Weather Fields)")
space = getattr(world, "space", None)
if space and hasattr(space, "snapshot"):
    ws = space.snapshot()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Ambient Light", ws.get("ambient_light", 0.0))
        st.metric("Darkness", ws.get("darkness", 0.0))
    with c2:
        st.metric("Temp (°C)", ws.get("temperature_c", 0.0))
        st.metric("Cloud", ws.get("cloud", 0.0))
    with c3:
        st.metric("Wind", ws.get("wind_level", 0.0))
        st.metric("Rain", str(ws.get("rain", False)))
    with c4:
        st.metric("Snow", str(ws.get("snow", False)))
        st.metric("Frame", ws.get("frame", 0))
else:
    st.warning("No WorldSpace present.")


# World State
st.subheader("World State")
st.json({
    "places": list(world.places.keys()),
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(getattr(world, "scouts", [])),
    "num_surveyors": len(getattr(world, "surveyors", [])),
})


# World Geometry & Objects
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
                    st.json(room.snapshot() if hasattr(room, "snapshot") else {"name": room.name})


# Walker visual (2D)
st.subheader("Walker (Motion)")
walker_snaps = []
for a in world.agents:
    if a.__class__.__name__ == "WalkerBot" and hasattr(a, "snapshot"):
        walker_snaps.append(a.snapshot())

if walker_snaps:
    wsnap = walker_snaps[0]
    st.json(wsnap)

    path = wsnap.get("path_tail", [])
    if path:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        ax.set_title("Walker path tail (x,y)")
        st.pyplot(fig)
else:
    st.info("No walker snapshot found.")


# Observer
st.subheader("Observer (Perception)")
obs_found = False
for a in world.agents:
    if a.__class__.__name__ == "ObserverBot" and hasattr(a, "snapshot"):
        obs_found = True
        st.json(a.snapshot())
if not obs_found:
    st.warning("No observer present.")


# Scouts
st.subheader("Scouts (Stakeouts)")
scouts = getattr(world, "scouts", [])
if not scouts:
    st.info("No scouts active.")
else:
    for sc in scouts:
        snap = sc.snapshot() or {}
        name = snap.get("name", "Scout")
        frame = snap.get("frame", "—")
        with st.expander(f"{name} · frame {frame}", expanded=False):
            st.json(snap)

            sound_tail = snap.get("sound_tail", [])
            if sound_tail:
                fig, ax = plt.subplots()
                ax.plot(sound_tail)
                ax.set_title("Scout sound tail")
                st.pyplot(fig)

            li_tail = snap.get("light_intensity_tail", [])
            if li_tail:
                fig, ax = plt.subplots()
                ax.plot(li_tail)
                ax.set_title("Scout light intensity tail")
                st.pyplot(fig)

            lc_tail = snap.get("light_color_tail", [])
            if lc_tail:
                st.write("Light colour tail:", lc_tail[-20:])


# Surveyors
st.subheader("Surveyors (Surfaces)")
surveyors = getattr(world, "surveyors", [])
if not surveyors:
    st.info("No surveyors active.")
else:
    for idx, sv in enumerate(surveyors):
        snap = sv.snapshot() or {}
        name = snap.get("name", f"Surveyor-{idx}")
        frame = snap.get("frame", "—")
        with st.expander(f"{name} · frame {frame}", expanded=False):
            occ = snap.get("occupancy_grid")
            surf = snap.get("surface_grid")

            col1, col2 = st.columns(2)
            with col1:
                st.write("Occupancy (solid)")
                if occ:
                    arr = np.array(occ)
                    fig, ax = plt.subplots()
                    ax.imshow(arr, cmap="gray")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No occupancy yet.")
            with col2:
                st.write("Surface edges")
                if surf:
                    arr = np.array(surf)
                    fig, ax = plt.subplots()
                    ax.imshow(arr, cmap="hot")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No surface yet.")


# Investigator (Accounting + Symbol Binding)
st.subheader("Salience Investigator (Accounting)")
inv = getattr(world, "salience_investigator", None)
if not inv:
    st.warning("No investigator present.")
else:
    inv_snap = inv.snapshot() if hasattr(inv, "snapshot") else {}
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Frames (Accounting)", inv_snap.get("frame_counter", 0))
        st.metric("Total Transactions", inv_snap.get("total_transactions", len(getattr(inv, "ledger", []))))
    with c2:
        st.json(inv_snap)

    ledger = getattr(inv, "ledger", [])
    if ledger:
        st.subheader("Recent Transactions (tail)")
        st.json(ledger[-10:])
    else:
        st.write("No ledger entries yet.")

st.caption("No words required • Fields and surfaces build evidence • Labels only after binding")