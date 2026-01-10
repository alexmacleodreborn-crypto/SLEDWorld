# pages/4_🔎_Scouts_Salience.py

import streamlit as st

st.title("🔎 Scouts (Salience Channels)")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

scouts = getattr(world, "scouts", [])
if not scouts:
    st.warning("No scouts registered.")
    st.stop()

for s in scouts:
    snap = s.snapshot() if hasattr(s, "snapshot") else {}
    with st.expander(f"{snap.get('name', 'Scout')} · {snap.get('focus','?')}", expanded=False):
        st.json(snap)