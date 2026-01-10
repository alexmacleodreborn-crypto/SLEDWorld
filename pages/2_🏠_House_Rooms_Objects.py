# pages/2_🏠_House_Rooms_Objects.py

import streamlit as st

st.title("🏠 House → Rooms → Objects")
world = st.session_state.get("world", None)
if world is None:
    st.warning("World not initialised. Go to Home page first.")
    st.stop()

places = getattr(world, "places", {})

# Find house-ish place with rooms
houses = []
for place in places.values():
    if hasattr(place, "rooms"):
        houses.append(place)

if not houses:
    st.warning("No house/places with rooms found.")
    st.stop()

for house in houses:
    st.subheader(f"Place: {getattr(house, 'name', 'Unknown')}")
    st.json(house.snapshot() if hasattr(house, "snapshot") else {"name": house.name})

    for room_name, room in house.rooms.items():
        with st.expander(f"Room: {room_name}", expanded=False):
            room_snap = room.snapshot() if hasattr(room, "snapshot") else {}
            st.json(room_snap)

            objs = getattr(room, "objects", {})
            st.write("Objects:", list(objs.keys()))

            # TV state quick view
            tv = objs.get("tv")
            if tv is not None:
                st.write("TV is_on:", getattr(tv, "is_on", None))
                # light if present
                if hasattr(tv, "light"):
                    st.write("TV light:", {"active": tv.light.active, "color": tv.light.color, "level": tv.light.level()})
                # sound if present
                if hasattr(tv, "sound"):
                    st.write("TV sound:", {"active": tv.sound.active, "level": tv.sound.level()})