import requests
import streamlit as st

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "your_openweathermap_api_key"  # Replace with your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -----------------------------
# WEATHER FUNCTION
# -----------------------------
def get_weather(city: str):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"].capitalize(),
            "rain": data.get("rain", {}).get("1h", 0),
        }
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="SkyCast – Your Smart Weather Companion", page_icon="🌤️")

st.title("🌤️ SkyCast – Your Smart Weather Companion")
st.markdown("Get real-time weather updates with temperature, humidity, rain forecast, and more.")

city = st.text_input("Enter City Name:")

if city:
    weather = get_weather(city)
    if "error" in weather:
        st.error(weather["error"])
    else:
        st.success(f"📍 Weather in {weather['city']}")
        st.metric("🌡️ Temperature", f"{weather['temperature']} °C")
        st.metric("💧 Humidity", f"{weather['humidity']} %")
        st.metric("🔽 Pressure", f"{weather['pressure']} hPa")
        st.metric("🌧️ Rain (last 1h)", f"{weather['rain']} mm")
        st.info(f"📋 Condition: {weather['description']}")

# Footer
st.markdown("---")
st.markdown("✨ Developed with ❤️ by [Rajed Mehmood](https://www.linkedin.com/in/rajedmehmood)")
