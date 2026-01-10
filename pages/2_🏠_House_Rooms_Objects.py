# pages/2_🏠_House_Rooms_Objects.py

st.title("House, Rooms & Objects")

for place in world.places.values():
    if hasattr(place, "rooms"):
        st.subheader(place.name)
        for room in place.rooms.values():
            st.json(room.snapshot())                    st.write("TV sound:", {"active": tv.sound.active, "level": tv.sound.level()})