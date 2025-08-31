import requests
import streamlit as st
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL_CURRENT = "https://api.open-meteo.com/v1/forecast"

# -----------------------------
# WEATHER FUNCTION
# -----------------------------
def get_current_weather(city: str):
    """Fetch current weather data using Open-Meteo with geocoding"""
    try:
        # Step 1: Get city coordinates via Open-Meteo geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10).json()
        if "results" not in geo_response:
            return {"error": "City not found. Please try another."}

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # Step 2: Get weather data
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation",
            "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(BASE_URL_CURRENT, params=params, timeout=10)
        data = response.json()

        return {"geo": geo_response["results"][0], "weather": data}
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="SkyCast – Your Smart Weather Companion", page_icon="🌤️")

st.title("🌤️ SkyCast – Your Smart Weather Companion")
st.markdown("Get real-time weather updates, forecasts, and more – powered by **Open-Meteo API (Free)** 🌍")

city = st.text_input("Enter City Name:")

if city:
    result = get_current_weather(city)

    if "error" in result:
        st.error(result["error"])
    else:
        geo = result["geo"]
        weather = result["weather"]

        st.success(f"📍 Weather in {geo['name']}, {geo.get('country','')}")

        # Current Weather
        current = weather["current_weather"]
        st.metric("🌡️ Temperature", f"{current['temperature']} °C")
        st.metric("💨 Wind Speed", f"{current['windspeed']} km/h")
        st.metric("🧭 Wind Direction", f"{current['winddirection']}°")

        # Forecast Section
        if st.button("📅 Show 3-Day Forecast"):
            st.subheader("3-Day Forecast")
            daily = weather["daily"]
            for i in range(3):
                st.write(
                    f"**{daily['time'][i]}**\n"
                    f"🌡️ Max: {daily['temperature_2m_max'][i]} °C | "
                    f"❄️ Min: {daily['temperature_2m_min'][i]} °C\n"
                    f"🌅 Sunrise: {daily['sunrise'][i].split('T')[1]} | "
                    f"🌇 Sunset: {daily['sunset'][i].split('T')[1]}\n"
                    f"🌧️ Precipitation: {daily['precipitation_sum'][i]} mm"
                )
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown("✨ Developed with ❤️ by [Rajed Mehmood](https://www.linkedin.com/in/rajedmehmood)")
