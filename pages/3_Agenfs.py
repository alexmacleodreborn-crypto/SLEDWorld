# pages/3_🚶_Agents.py

import streamlit as st

st.title("🚶 Agents (Walker / Observer)")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

agents = getattr(world, "agents", [])
st.write("Agents:", [a.__class__.__name__ for a in agents])

for agent in agents:
    with st.expander(f"{agent.__class__.__name__}", expanded=False):
        if hasattr(agent, "snapshot"):
            st.json(agent.snapshot())
        else:
            st.write("No snapshot() available.")