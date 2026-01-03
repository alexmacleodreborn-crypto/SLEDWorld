with c3:
    ticks = st.number_input("awake ticks (window)", min_value=5, max_value=200, value=20, step=5)
    if st.button("▶ Run Awake Window"):
        cycle.run_day_window(n_ticks=int(ticks))

with c4:
    if st.button("🌙 Sleep → Next Day"):
        cycle.sleep_and_advance()