# pages/5_📒_Ledger.py

import streamlit as st

st.title("📒 Ledger (Truth / Transactions)")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

ledger = getattr(world, "salience_investigator", None)
if ledger is None:
    st.warning("No salience investigator present.")
    st.stop()

st.subheader("Ledger Snapshot")
if hasattr(ledger, "snapshot"):
    st.json(ledger.snapshot())
else:
    st.write("No snapshot() method on ledger.")

st.subheader("Recent Entries")
entries = getattr(ledger, "ledger", [])
n = st.slider("Show last N", 5, 200, 25)
st.json(entries[-n:] if entries else [])