import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

st.set_page_config(page_title="SLED World – A7DO Prebirth", layout="wide")
st.title("🧠 SLED World – A7DO Pre-Birth → Birth → Post-Birth")

# Session state
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()
if "cycle" not in st.session_state:
    st.session_state.cycle = DayCycle(st.session_state.a7do)

a7do = st.session_state.a7do
cycle = st.session_state.cycle

c1, c2, c3 = st.columns([1.2, 1.2, 2.2])

with c1:
    st.subheader("🎛 Controls")

    pre_ticks = st.number_input("Prebirth ticks", min_value=10, max_value=300, value=30, step=10)
    if st.button("🫧 Run Prebirth Growth Window"):
        cycle.run_prebirth_window(n_ticks=int(pre_ticks))

    st.divider()

    if st.button("👶 Trigger Birth Transition"):
        cycle.trigger_birth()

    st.divider()

    post_place = st.selectbox("Postbirth place", ["home", "hospital"])
    post_ticks = st.number_input("Postbirth ticks", min_value=5, max_value=200, value=20, step=5)
    if st.button("▶ Run Postbirth Window"):
        cycle.run_postbirth_window(place=post_place, n_ticks=int(post_ticks))

    if st.button("🌙 Sleep & Consolidate → Next Day"):
        cycle.sleep_and_consolidate()

with c2:
    st.subheader("🧍 Internal State")
    st.write(f"**Exists:** {a7do.exists}")
    st.write(f"**Birthed:** {a7do.birthed}")
    st.write(f"**Day:** {a7do.day}")
    st.write(f"**Current place (perceived):** {a7do.world.current_place}")

    st.divider()
    st.write("**Growth**")
    st.metric("Sensory gain", f"{a7do.body.sensory_gain:.2f}")
    st.metric("Motor strength", f"{a7do.body.motor_strength:.2f}")
    st.metric("Reflex rate", f"{a7do.body.reflex_rate:.2f}")

    st.divider()
    st.write("**Drives**")
    st.progress(a7do.body.hunger, text=f"Hunger: {a7do.body.hunger:.2f}")
    st.progress(a7do.body.wetness, text=f"Wetness: {a7do.body.wetness:.2f}")
    st.progress(a7do.body.fatigue, text=f"Fatigue: {a7do.body.fatigue:.2f}")
    st.progress(min(1.0, a7do.body.arousal / 2.0), text=f"Arousal: {a7do.body.arousal:.2f}")

    st.divider()
    st.write("**Familiarity (Top patterns)**")
    for pat, score in a7do.familiarity.top(6):
        st.write(f"- {pat}: {score:.2f}")

with c3:
    st.subheader("📜 Observer Log (latest 80)")
    if not a7do.log.entries:
        st.info("No events yet.")
    else:
        for entry in reversed(a7do.log.entries[-80:]):
            st.write(entry)