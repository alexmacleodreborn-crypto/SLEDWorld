st.title("Scouts & Salience")

for scout in getattr(world, "scouts", []):
    st.json(scout.snapshot())