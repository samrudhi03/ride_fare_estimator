import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
from src.locations import area_coordinates
import folium
from streamlit_folium import st_folium
import datetime
import openrouteservice

# ORS API Key
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijk4YWUzMjY5YTQ1ZDRiMzU4YTE5OWFlY2M5ODZjZmFmIiwiaCI6Im11cm11cjY0In0="
ors_client = openrouteservice.Client(key=ORS_API_KEY)

# Session state
if "fare_data" not in st.session_state:
    st.session_state.fare_data = None

# Sidebar inputs
st.sidebar.header("Ride Details")
pickup_area = st.sidebar.selectbox("Select Pickup Area", list(area_coordinates.keys()))
dropoff_area = st.sidebar.selectbox("Select Dropoff Area", list(area_coordinates.keys()))
passenger_count = st.sidebar.number_input("Number of Passengers", min_value=1, max_value=6, value=1)
ride_time = st.sidebar.time_input("Select Pickup Time", value=datetime.time(12, 0))
ride_date = st.sidebar.date_input("Select Pickup Date", value=datetime.date.today())

# Submit button
if st.sidebar.button("Estimate Fare"):
    url = "http://127.0.0.1:8000/predict"
    input_data = {
        "pickup_area": pickup_area,
        "dropoff_area": dropoff_area,
        "passenger_count": passenger_count,
        "hour": ride_time.hour,
        "day": ride_date.day
    }

    response = requests.post(url, json=input_data)

    if response.status_code == 200:
        result = response.json()
        st.session_state.fare_data = {
            "fare": result["fare_amount"],
            "pickup_area": pickup_area,
            "dropoff_area": dropoff_area,
            "ride_date": ride_date,
            "ride_time": ride_time,
            "passenger_count": passenger_count,
            "pickup_coords": result["pickup_coords"],
            "dropoff_coords": result["dropoff_coords"]
        }
    else:
        st.error("Failed to estimate fare. Please try again.")

# Display result
if st.session_state.fare_data:
    data = st.session_state.fare_data

    st.markdown("## 🚕 Your Uber Ride Estimate")
    st.markdown(f"""
    **Pickup Location:** {data["pickup_area"]}  
    **Dropoff Location:** {data["dropoff_area"]}  
    **Date:** {data["ride_date"].strftime("%Y-%m-%d")}  
    **Time:** {data["ride_time"].strftime("%H:%M")}  
    **Passengers:** {data["passenger_count"]}  
    **Estimated Fare:** 💰 ${data["fare"]}  
    """)

    # Map
    m = folium.Map(location=data["pickup_coords"][::-1], zoom_start=12)

    folium.Marker(data["pickup_coords"][::-1], tooltip="Pickup", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(data["dropoff_coords"][::-1], tooltip="Dropoff", icon=folium.Icon(color="red")).add_to(m)

    coords = (
        data["pickup_coords"],
        data["dropoff_coords"]
    )

    try:
        # Optional snapping (uncomment if needed):
        # start_snap = ors_client.nearest(coordinates=[coords[0]], profile="driving-car")["features"][0]["geometry"]["coordinates"]
        # end_snap = ors_client.nearest(coordinates=[coords[1]], profile="driving-car")["features"][0]["geometry"]["coordinates"]
        # coords = [start_snap, end_snap]

        # Request route with increased search radius
        route = ors_client.directions(
            coords,
            profile="driving-car",
            radiuses=[1000, 1000]  # meters
        )
        geometry = route['routes'][0]['geometry']
        decoded = openrouteservice.convert.decode_polyline(geometry)
        route_coords = [(lat, lon) for lon, lat in decoded['coordinates']]
        folium.PolyLine(route_coords, color="blue", weight=4, opacity=0.7).add_to(m)

    except Exception as e:
        st.warning(f"Could not draw route: {e}")
        # Fallback to straight line
        folium.PolyLine([
            data["pickup_coords"][::-1],
            data["dropoff_coords"][::-1]
        ], color="gray").add_to(m)

    st_folium(m, width=700, height=500)

else:
    st.markdown("## 🚕 Welcome to Ride Fare Estimator")
    st.markdown("""
    Use the sidebar to input your ride details.  
    You'll see a map and fare estimate here, just like Uber!  
    """)

    default_center = [40.7128, -74.0060]  # NYC center
    default_map = folium.Map(location=default_center, zoom_start=11)
    st_folium(default_map, width=700, height=500)
