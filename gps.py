import streamlit as st
from streamlit_js_eval import streamlit_js_eval

def get_gps_location():
    """
    Uses the browser's Geolocation API.
    """

    location = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude
                }),
                (err) => resolve(null)
            );
        })
        """,
        key="gps"
    )

    return location