import requests
from math import radians, sin, cos, sqrt, atan2


def distance(lat1, lon1, lat2, lon2):

    R = 6371

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)

    a = sin(dLat / 2) ** 2 + \
        cos(radians(lat1)) * \
        cos(radians(lat2)) * \
        sin(dLon / 2) ** 2

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(R * c, 2)


def get_bus_stops(lat, lon):

    query = f"""
    [out:json];
    (
      node["highway"="bus_stop"](around:1000,{lat},{lon});
    );
    out body;
    """

    response = requests.get(
        ""https://lz4.overpass-api.de/api/interpreter",
        params={"data": query},
        timeout=30
    )

    data = response.json()

    stops = []

    for stop in data.get("elements", []):

        stop_lat = stop["lat"]
        stop_lon = stop["lon"]

        stops.append({

            "name": stop.get(
                "tags",
                {}
            ).get(
                "name",
                "Unnamed Bus Stop"
            ),

            "latitude": stop_lat,
            "longitude": stop_lon,

            "distance":
            distance(
                lat,
                lon,
                stop_lat,
                stop_lon
            )
        })

    stops.sort(
        key=lambda x: x["distance"]
    )

    return stops
