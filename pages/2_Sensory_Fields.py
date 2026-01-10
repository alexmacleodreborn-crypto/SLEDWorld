import streamlit as st

st.set_page_config(layout="wide")
st.title("Sensory Fields — Sound & Light")

world = st.session_state.get("world")
if not world:
    st.warning("Advance the world from the Manager page.")
    st.stop()

for scout in world.scouts:
    snap = scout.snapshot()
    with st.expander(f"{snap.get('name')} ({snap.get('mode')})"):
        st.json(snap.get("summary"))
        st.write("Grid (intensity map):")
        st.dataframe(snap.get("grid", []))