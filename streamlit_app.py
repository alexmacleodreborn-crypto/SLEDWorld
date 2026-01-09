import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLEDWorld – Reality Frame", layout="wide")

# -----------------------
# Session init
# -----------------------
if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

clock = st.session_state.clock
world = st.session_state.world

# -----------------------
# Sidebar
# -----------------------
st.sidebar.header("World Control")

advance_steps = st.sidebar.slider("Advance steps", 1, 50, 5)
minutes_per_step = st.sidebar.slider("Minutes per step", 1, 30, 1)

auto = st.sidebar.checkbox("Auto-run", value=False)
auto_delay = st.sidebar.slider("Auto delay (sec)", 0.1, 2.0, 0.3, 0.1)

if st.sidebar.button("▶ Advance"):
    for _ in range(advance_steps):
        clock.tick(minutes=minutes_per_step)
        world.tick()

if st.sidebar.button("Reset World"):
    st.session_state.pop("world", None)
    st.session_state.pop("clock", None)
    st.rerun()

if auto:
    # light auto loop: reruns page; state persists in session_state
    clock.tick(minutes=minutes_per_step)
    world.tick()
    st.sidebar.caption("Auto running… (state persists)")
    st.sidebar.write("")
    st.rerun()

# -----------------------
# Main
# -----------------------
st.title("SLEDWorld – Reality Frame")
st.caption("World Genesis Stack • Structure → Signals → Ledger → Symbols (No minds yet)")

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("Clock")
    st.json(clock.snapshot())

with colB:
    st.subheader("World Summary")
    st.json({
        "frame": getattr(world, "frame", None),
        "num_places": len(world.places),
        "place_names": list(world.places.keys()),
        "num_agents": len(world.agents),
        "num_scouts": len(world.scouts),
    })

# -----------------------
# Places / Rooms / Objects
# -----------------------
st.subheader("Places, Rooms, Objects")

for place in world.places.values():
    with st.expander(f"Place: {place.name}", expanded=False):
        st.json(place.snapshot())

        if hasattr(place, "rooms"):
            for room in place.rooms.values():
                with st.expander(f"Room: {room.name}", expanded=False):
                    st.json(room.snapshot())

# -----------------------
# Bots
# -----------------------
st.subheader("Bots")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### Walker")
    w = world.get_agent("WalkerBot")
    st.json(w.snapshot() if w else {"missing": "WalkerBot"})

with c2:
    st.markdown("### Observer")
    o = world.get_agent("ObserverBot")
    st.json(o.snapshot() if o else {"missing": "ObserverBot"})

with c3:
    st.markdown("### Surveyor")
    s = world.surveyor
    st.json({
        "name": s.name,
        "frame": s.frames,
        "active": s.active,
        "center_xyz": s.center_xyz,
        "resolution_m": s.resolution_m,
        "volume_shape": s.last_snapshot.get("volume_shape") if s.last_snapshot else None,
    })

# -----------------------
# Aerial 2D (1/0)
# -----------------------
st.subheader("Aerial Occupancy (1=solid column, 0=empty)")

surv_snap = world.surveyor.snapshot()
aerial = None
if isinstance(surv_snap, dict):
    aerial = surv_snap.get("aerial_grid")

if aerial is None:
    st.warning("No aerial grid yet (advance a few frames).")
else:
    arr = np.array(aerial, dtype=float)
    fig, ax = plt.subplots()
    ax.imshow(arr, interpolation="nearest")
    ax.set_title("Top-down occupancy")
    ax.axis("off")
    st.pyplot(fig)

# -----------------------
# Scouts
# -----------------------
st.subheader("Scouts")

if world.scouts:
    for scout in world.scouts:
        snap = scout.snapshot()
        with st.expander(f"{snap.get('name','scout')} · {snap.get('signal')} · frame {snap.get('frame')}", expanded=False):
            st.json({k: v for k, v in snap.items() if k not in ("grid",)})
            grid = snap.get("grid")
            if grid is not None:
                arr = np.array(grid, dtype=float)
                fig, ax = plt.subplots()
                ax.imshow(arr, interpolation="nearest")
                ax.axis("off")
                st.pyplot(fig)
else:
    st.write("No active scouts (ledger will deploy them on detected changes).")

# -----------------------
# Ledger / Promotions / Language
# -----------------------
st.subheader("Ledger (Truth)")

ledger = world.ledger
left, right = st.columns([1, 1])

with left:
    st.metric("Frames Processed", ledger.frame_counter)
    st.metric("Transactions", len(ledger.ledger))
    st.metric("Symbols", len(ledger.symbols))
    st.metric("Lexicon", len(world.language.lexicon))

with right:
    st.json(ledger.snapshot())

st.markdown("### Recent Transactions (tail)")
tail = ledger.ledger[-15:] if ledger.ledger else []
st.json(tail if tail else {"empty": True})

st.markdown("### Symbols (current)")
st.json(ledger.symbols)

st.markdown("### Language (grounded words)")
st.json(world.language.snapshot())

st.caption("Reality exists first • Bots compile structure • Ledger promotes symbols • Words bind only after grounding")