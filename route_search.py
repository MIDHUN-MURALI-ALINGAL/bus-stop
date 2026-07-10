import streamlit as st

from route_utils import search_route


def search_page():

    st.header("🚌 Find Private Bus")

    source = st.text_input("From")

    destination = st.text_input("To")

    if st.button("Search Bus"):

        buses = search_route(

            source,

            destination

        )

        if len(buses)==0:

            st.warning("No buses found.")

        else:

            for bus in buses:

                st.success(bus[0])

                st.write("Bus Number :",bus[1])

                st.write("Route :",bus[2],"→",bus[3])

                st.write("Fare : ₹",bus[4])

                st.write("Travel Time :",bus[5])

                st.divider()