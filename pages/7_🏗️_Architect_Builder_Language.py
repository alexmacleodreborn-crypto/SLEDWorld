st.title("Architect · Builder · Language")

if hasattr(world, "architect"):
    st.subheader("Architect")
    st.json(world.architect.snapshot())

if hasattr(world, "builder"):
    st.subheader("Builder")
    st.json(world.builder.snapshot())

if hasattr(world, "language"):
    st.subheader("Language")
    st.json(world.language.snapshot())