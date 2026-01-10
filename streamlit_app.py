import streamlit as st
from world_core.bootstrap import build_world
from world_core.world_clock import WorldClock

st.set_page_config(page_title="SLEDWorld — Manager", layout="wide")
st.title("SLEDWorld — Manager Overview")
st.caption("Investigate → Ledger → Language → Ledger → Manager • Square-gated")

if "clock" not in st.session_state:
    st.session_state.clock = WorldClock(acceleration=1)

if "world" not in st.session_state:
    st.session_state.world = build_world(st.session_state.clock)

world = st.session_state.world

st.divider()
c1, c2, c3 = st.columns([1,1,2])
with c1:
    steps = st.number_input("Advance steps", 1, 100, 1)
with c2:
    if st.button("▶ Advance"):
        for _ in range(int(steps)):
            world.tick()
with c3:
    if st.button("Reset World"):
        st.session_state.pop("world", None)
        st.session_state.pop("clock", None)
        st.rerun()

st.divider()
colA, colB, colC, colD = st.columns(4)
colA.metric("Frame", world.frame)
colB.metric("Places", len(world.places))
colC.metric("Agents", len(world.agents))
colD.metric("Scouts", len(world.scouts))

st.subheader("Ledger Gates (Sandy’s Law + SandySquare)")
st.json(world.ledger.snapshot())

st.subheader("Manager Decisions (tail)")
st.json(world.manager.snapshot())

st.subheader("Reception Directory")
st.json(world.reception.snapshot())

st.subheader("Concierge Proposals")
st.json(world.concierge.snapshot())

st.subheader("Language State")
st.json(world.language.snapshot())

st.subheader("Ledger Tail (latest)")
st.json(world.ledger.tail(25))