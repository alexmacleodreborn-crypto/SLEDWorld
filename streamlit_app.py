# -------------------------
# Observer Control
# -------------------------

st.sidebar.header("Observer Control")

if not cycle.has_birthed:
    if st.sidebar.button("Run Pre-birth Cycle"):
        cycle.prebirth_cycle()

    st.sidebar.caption(
        f"Gestation cycles: {a7do.gestation_cycles} / 180"
    )
else:
    if st.sidebar.button("Wake"):
        cycle.wake()

    if st.sidebar.button("Sleep"):
        cycle.sleep()
        cycle.next_day()

# Perception mode (post-birth only)
if a7do.birthed:
    modes = ["hospital", "home"]
    selected = st.sidebar.selectbox(
        "A7DO perception mode",
        modes,
        index=modes.index(a7do.perception_mode)
    )
    a7do.perception_mode = selected
else:
    st.sidebar.info("Pre-birth: perception locked to womb")