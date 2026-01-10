st.title("Ledger")

ledger = world.ledger
st.metric("Total Events", len(ledger.events))
st.json(ledger.events[-20:])