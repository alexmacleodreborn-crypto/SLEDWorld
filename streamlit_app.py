# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock


st.set_page_config(page_title="SLEDWorld – Pattern → Symbols → Language", layout="wide")
st.title("SLEDWorld – Pattern → Symbols → Language")
st.caption("World → Surveyor (surfaces) → Ledger (promotion) → Architect/Builder (structure) → Language (tokens)")

# ----------------------------
# Session init
# ----------------------------
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Advance")
steps = st.sidebar.slider("Steps", 1, 80, 10)
if st.sidebar.button("▶ Advance World"):
    for _ in range(steps):
        clock.tick(minutes=1)
        world.tick()

st.sidebar.divider()
if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

# ----------------------------
# World summary
# ----------------------------
st.subheader("World Summary")
st.json({
    "world_frame": world.frame,
    "num_places": len(world.places),
    "num_agents": len(world.agents),
    "num_scouts": len(world.scouts),
    "has_surveyor": world.surveyor is not None,
})

# ----------------------------
# World geometry (places/rooms/objects)
# ----------------------------
st.subheader("World Geometry & Objects")
for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json({
            "position": getattr(place, "position", None),
            "bounds": getattr(place, "bounds", None),
        })

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                rs = room.snapshot()
                with st.expander(f"Room: {room.name} ({rs.get('room_type')})", expanded=False):
                    st.json({
                        "bounds": rs.get("bounds"),
                        "signals": rs.get("signals"),
                        "objects": rs.get("objects", {}),
                    })

# ----------------------------
# Agents
# ----------------------------
st.subheader("Agents")
for a in world.agents:
    if hasattr(a, "snapshot"):
        st.json(a.snapshot())

# ----------------------------
# Scouts
# ----------------------------
st.subheader("Scouts (local shape/sound/light)")
show_occ = st.toggle("Show Occupancy", value=True)
show_sound = st.toggle("Show Sound", value=True)
show_light = st.toggle("Show Light", value=True)

for s in world.scouts:
    snap = s.snapshot()
    with st.expander(f"{snap.get('name')} · frame {snap.get('frame')} · area {snap.get('area')}", expanded=False):
        st.json(snap)

        cols = st.columns(3)
        if show_occ:
            with cols[0]:
                fig, ax = plt.subplots()
                ax.imshow(s.occupancy, cmap="gray")
                ax.set_title("Occupancy")
                ax.axis("off")
                st.pyplot(fig)

        if show_sound:
            with cols[1]:
                fig, ax = plt.subplots()
                ax.imshow(s.sound, cmap="viridis")
                ax.set_title("Sound field")
                ax.axis("off")
                st.pyplot(fig)

        if show_light:
            with cols[2]:
                fig, ax = plt.subplots()
                ax.imshow(s.light, cmap="inferno")
                ax.set_title("Light field")
                ax.axis("off")
                st.pyplot(fig)

# ----------------------------
# Surveyor visuals (safe projections)
# ----------------------------
st.subheader("Surveyor – Surface Projections")
if world.surveyor is None:
    st.warning("No surveyor present.")
else:
    ss = world.surveyor.snapshot()
    surf = ss.get("surface_volume", None)
    vol = ss.get("volume", None)

    if surf is None or vol is None:
        st.info("Advance world to generate surveyor volume.")
    else:
        surf_np = np.array(surf, dtype=np.uint8)  # z,y,x
        vol_np = np.array(vol, dtype=np.uint8)

        # Top-down projection: max across z
        top = surf_np.max(axis=0)

        # Choose 3 z-slices (floor-ish, mid, high)
        nz = surf_np.shape[0]
        z_idxs = [
            min(nz-1, max(0, nz//6)),
            min(nz-1, max(0, nz//2)),
            min(nz-1, max(0, (5*nz)//6)),
        ]

        colA, colB = st.columns([1.2, 1.0])

        with colA:
            st.caption("Top-down surface map")
            fig, ax = plt.subplots()
            ax.imshow(top, cmap="gray")
            ax.axis("off")
            st.pyplot(fig)

        with colB:
            st.caption(f"Surveyor geometry summary (planes)")
            st.json(world.ledger.geom)

        st.caption("Z-slices (surfaces)")
        c1, c2, c3 = st.columns(3)
        for col, zi in zip([c1, c2, c3], z_idxs):
            with col:
                fig, ax = plt.subplots()
                ax.imshow(surf_np[zi], cmap="gray")
                ax.set_title(f"z slice {zi}")
                ax.axis("off")
                st.pyplot(fig)

# ----------------------------
# Ledger promotions
# ----------------------------
st.subheader("Ledger (Promotion Engine)")
ledger_snap = world.ledger.snapshot()

col1, col2 = st.columns(2)
with col1:
    st.metric("Frames", ledger_snap.get("frame", 0))
    st.metric("Entries", ledger_snap.get("total_entries", 0))
    st.metric("Transitions", ledger_snap.get("total_transitions", 0))

with col2:
    st.json({
        "symbols": ledger_snap.get("symbols", {}).get("types", {}),
        "geom_planes": ledger_snap.get("geom", {}).get("planes", {}),
    })

st.subheader("Transitions (tail)")
st.json(ledger_snap.get("transitions_tail", []))

# ----------------------------
# Architect / Builder
# ----------------------------
st.subheader("Architect + Builder")
st.json(world.architect.snapshot())
st.json(world.builder.snapshot())

# ----------------------------
# Language (tokens)
# ----------------------------
st.subheader("Language (tokens emerge after symbols)")
lang = world.language.snapshot()
st.json({
    "lexicon": lang.get("lexicon", {}),
    "utterances_tail": lang.get("utterances_tail", []),
})

st.caption("Advance 30–90 steps: Walker toggles TV periodically → light/sound transitions → TV symbol → language tokens (TV ON/OFF, RED/GREEN).")