import streamlit as st
from auth import (
    initialize_session,
    login,
    register,
    profile,
    logout
)
from gps import get_gps_location
from bus_stop import get_bus_stops
from map_utils import show_map
# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="Smart Public Transport Assistant",
    page_icon="🚌",
    layout="wide"
)

# --------------------------
# Initialize Session
# --------------------------
initialize_session()

# --------------------------
# If User NOT Logged In
# --------------------------
if not st.session_state.logged_in:

    st.sidebar.title("Navigation")

    menu = st.sidebar.radio(
        "Select",
        [
            "Login",
            "Register"
        ]
    )

    if menu == "Login":
        login()

    else:
        register()

    st.stop()

# --------------------------
# Sidebar
# --------------------------
st.sidebar.title("🚍 Smart Public Transport")

st.sidebar.success(
    f"Welcome {st.session_state.user['fullname']}"
)

page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Profile",
        "History",
        "Favourite Stops",
        "Settings"
    ]
)

if st.sidebar.button("Logout"):
    logout()

# --------------------------
# --------------------------
# Dashboard
# --------------------------

if page == "Dashboard":

    st.title("🚌 Smart Public Transport Assistant")

    st.success(
        f"Welcome {st.session_state.user['fullname']} 👋"
    )

    st.write("### 📍 Detecting your location...")

    location = get_gps_location()

    if location is None:

        st.warning("Please allow location access.")

        st.stop()

    latitude = location["latitude"]
    longitude = location["longitude"]

    st.success("Current Location Detected")

    st.write(f"Latitude : {latitude}")

    st.write(f"Longitude : {longitude}")

    st.write("---")

    st.subheader("Nearby Bus Stops")

    with st.spinner("Searching nearby bus stops..."):

        bus_stops = get_bus_stops(
            latitude,
            longitude
        )

    if len(bus_stops) == 0:

        st.warning("No Bus Stops Found.")

    else:

        for stop in bus_stops:

            st.write(
                f"""
🚌 **{stop['name']}**

📏 Distance : **{stop['distance']} km**
"""
            )

        show_map(
            latitude,
            longitude,
            bus_stops
        )

# --------------------------
# Profile
# --------------------------
elif page == "Profile":

    profile()

# --------------------------
# Search History
# --------------------------
elif page == "History":

    st.title("📜 Search History")

    st.info(
        "No searches yet."
    )

# --------------------------
# Favourite Stops
# --------------------------
elif page == "Favourite Stops":

    st.title("⭐ Favourite Bus Stops")

    st.info(
        "No favourite stops added."
    )

# --------------------------
# Settings
# --------------------------
elif page == "Settings":

    st.title("⚙ Settings")

    st.write("Dark Mode (Coming Soon)")

    st.write("Language (Coming Soon)")