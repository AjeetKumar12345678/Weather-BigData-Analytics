import streamlit as st
import pandas as pd

from weather_api import get_location, get_weather
from spark_analysis import analyze_weather


st.set_page_config(
    page_title="Weather Big Data Analytics",
    page_icon="🌤️",
    layout="wide"
)


# -----------------------------
# HEADER
# -----------------------------

st.title("🌤️ Weather Big Data Analytics")

st.write(
    "Real-Time Weather Analysis using "
    "Open-Meteo API and PySpark"
)


# -----------------------------
# LOCATION SEARCH
# -----------------------------

location = st.text_input(
    "Enter Location",
    placeholder="Example: Mumbai, Delhi, London, New York"
)


analyze = st.button(
    "🔍 Get Current Weather",
    use_container_width=True
)


if analyze:

    if location.strip() == "":
        st.warning("Please enter a location.")

    else:

        try:

            with st.spinner("Fetching real-time weather data..."):

                # Get coordinates
                location_data = get_location(location)

                if location_data is None:
                    st.error("Location not found.")
                    st.stop()

                latitude = location_data["latitude"]
                longitude = location_data["longitude"]

                # Get weather
                weather = get_weather(
                    latitude,
                    longitude
                )

                current = weather["current"]


            # -----------------------------
            # LOCATION
            # -----------------------------

            st.success(
                f"Weather for "
                f"{location_data['name']}, "
                f"{location_data['country']}"
            )

            st.caption(
                f"Coordinates: "
                f"{latitude:.4f}, {longitude:.4f}"
            )


            # -----------------------------
            # CURRENT WEATHER
            # -----------------------------

            st.subheader("🌡️ Current Weather")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Temperature",
                f"{current['temperature_2m']} °C"
            )

            col2.metric(
                "Feels Like",
                f"{current['apparent_temperature']} °C"
            )

            col3.metric(
                "Humidity",
                f"{current['relative_humidity_2m']} %"
            )

            col4.metric(
                "Wind Speed",
                f"{current['wind_speed_10m']} km/h"
            )


            col5, col6, col7, col8 = st.columns(4)

            col5.metric(
                "Rainfall",
                f"{current['precipitation']} mm"
            )

            col6.metric(
                "Cloud Cover",
                f"{current['cloud_cover']} %"
            )

            col7.metric(
                "Pressure",
                f"{current['surface_pressure']} hPa"
            )

            col8.metric(
                "Wind Direction",
                f"{current['wind_direction_10m']}°"
            )


            # -----------------------------
            # PYSPARK ANALYSIS
            # -----------------------------

            st.subheader("📊 Big Data Analysis")

            analysis = analyze_weather(weather)

            a, b, c = st.columns(3)

            a.metric(
                "Average Temperature",
                f"{analysis['avg_temperature']} °C"
            )

            b.metric(
                "Maximum Temperature",
                f"{analysis['max_temperature']} °C"
            )

            c.metric(
                "Minimum Temperature",
                f"{analysis['min_temperature']} °C"
            )


            d, e, f = st.columns(3)

            d.metric(
                "Average Humidity",
                f"{analysis['avg_humidity']} %"
            )

            e.metric(
                "Average Wind Speed",
                f"{analysis['avg_wind_speed']} km/h"
            )

            f.metric(
                "Average Rainfall",
                f"{analysis['avg_rainfall']} mm"
            )


            # -----------------------------
            # HOURLY DATA
            # -----------------------------

            hourly = weather["hourly"]

            df = pd.DataFrame({

                "Time": hourly["time"],

                "Temperature (°C)":
                    hourly["temperature_2m"],

                "Humidity (%)":
                    hourly["relative_humidity_2m"],

                "Rainfall (mm)":
                    hourly["precipitation"],

                "Wind Speed (km/h)":
                    hourly["wind_speed_10m"]
            })


            df["Time"] = pd.to_datetime(df["Time"])


            # -----------------------------
            # CHARTS
            # -----------------------------

            st.subheader("📈 Temperature Trend")

            st.line_chart(
                df.set_index("Time")[
                    ["Temperature (°C)"]
                ]
            )


            st.subheader("💧 Humidity Trend")

            st.line_chart(
                df.set_index("Time")[
                    ["Humidity (%)"]
                ]
            )


            st.subheader("💨 Wind Speed Trend")

            st.line_chart(
                df.set_index("Time")[
                    ["Wind Speed (km/h)"]
                ]
            )


            st.subheader("🌧️ Rainfall Trend")

            st.bar_chart(
                df.set_index("Time")[
                    ["Rainfall (mm)"]
                ]
            )


            # -----------------------------
            # DATA TABLE
            # -----------------------------

            st.subheader("📋 Weather Data")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


        except Exception as error:

            st.error(
                f"Unable to fetch weather data: {error}"
            )