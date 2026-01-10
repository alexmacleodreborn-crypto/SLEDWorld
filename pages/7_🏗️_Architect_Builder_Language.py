# pages/7_🏗️_Architect_Builder_Language.py

import streamlit as st

st.title("🏗️ Architect / Builder / Language (Read-only)")

world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

wanted = {"ArchitectBot", "BuilderBot", "LanguageBot"}
found = [a for a in getattr(world, "agents", []) if a.__class__.__name__ in wanted]

if not found:
    st.info("Bots not attached yet. (That’s fine.) When ready, add them to bootstrap as agents.")
    st.stop()

for bot in found:
    with st.expander(bot.__class__.__name__, expanded=True):
        st.json(bot.snapshot() if hasattr(bot, "snapshot") else {})