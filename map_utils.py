import folium
from streamlit_folium import st_folium


def show_map(
    lat,
    lon,
    bus_stops
):

    m = folium.Map(
        location=[lat, lon],
        zoom_start=16
    )

    folium.Marker(
        [lat, lon],
        popup="You are here",
        icon=folium.Icon(
            color="red"
        )
    ).add_to(m)

    for stop in bus_stops:

        folium.Marker(
            [
                stop["latitude"],
                stop["longitude"]
            ],

            popup=f"""
            {stop['name']}

            {stop['distance']} km
            """,

            icon=folium.Icon(
                color="blue",
                icon="bus",
                prefix="fa"
            )

        ).add_to(m)

    st_folium(
        m,
        width=1000,
        height=600
    )